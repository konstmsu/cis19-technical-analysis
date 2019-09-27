import json
from typing import cast

# pylint: disable=redefined-outer-name,unused-import
from test.flask_testing import test_client
import responses
import requests
import pytest
import app


def test_instructions(test_client):
    for url in ["/", "/instructions"]:
        response = test_client.get(url, follow_redirects=True)
        assert b"function family" in response.data
        assert b'class="input"' not in response.data


def test_instructions_style(test_client):
    response = test_client.get("/custom.css")
    assert b".prompt" in response.data


def test_favicon(test_client):
    response = test_client.get("/favicon.ico")
    assert int(response.headers["Content-Length"]) == 1406


class _EvaluationContext:
    def __init__(self, test_client):
        self.test_client = test_client
        self.team_url = "https://solver"
        self.evaluate_callback_url = "https://codeit-suisse/evaluate-callback"
        self.solver_response_status = 200

    @property
    def solver_url(self):
        return f"{self.team_url}/technical-analysis"

    def add_solver_response(self, status, body):
        responses.add(responses.POST, self.solver_url, status=status, body=body)

    def add_evaluate_callback(self, status):
        responses.add(
            responses.POST,
            self.evaluate_callback_url,
            status=status,
            body="result recorded",
        )

    def evaluate(self, use_test_challenge: bool):
        response = self.test_client.post(
            "/evaluate",
            json={
                "teamUrl": self.team_url,
                "callbackUrl": self.evaluate_callback_url,
                "runId": "142",
                "isTest": use_test_challenge,
            },
        )
        assert response.status == "200 OK"
        assert response.get_json() == {"callback_result": "b'result recorded'"}
        return self.get_evaluate_call()

    def get_evaluate_call(self):
        evaluate_call = responses.calls[1]
        assert evaluate_call.request.url == self.evaluate_callback_url
        return evaluate_call


def _run_solver(
    test_client,
    solver_status_code: int,
    solver_result,
    use_test_challenge: bool = False,
):
    context = _EvaluationContext(test_client)
    context.add_solver_response(solver_status_code, solver_result)
    context.add_evaluate_callback(200)
    request: requests.PreparedRequest = context.evaluate(
        use_test_challenge=use_test_challenge
    ).request

    evaluation = json.loads(cast(bytes, request.body).decode("utf-8"))

    assert evaluation["runId"] == "142"

    return evaluation


@responses.activate
def test_solver_feature_toggle(test_client):
    response = test_client.get("/technical-analysis")
    assert response.status_code == 405
    # TODO
    # assert b"Solver is not enabled" in response.data


@responses.activate
def test_solution_error(test_client):
    evaluation = _run_solver(test_client, 503, "Some internal error")
    assert evaluation["score"] == 0
    assert (
        "Error: Got 503 from solver https://solver/technical-analysis. Some internal error"
        in evaluation["message"]
    )


@responses.activate
def test_solution_wrong_format(test_client):
    evaluation = _run_solver(test_client, 200, "some non-json")
    assert evaluation["score"] == 0
    assert "Error: Failed to parse json <some non-json>" in evaluation["message"]


# TODO I'm not sure how much state there is in the test_client so doing one test per method


@responses.activate
def test_solution_invalid_json_payload1(test_client):
    evaluation = _run_solver(test_client, 200, "}")
    assert evaluation["score"] == 0
    assert "Error: Failed to parse json <}>" in evaluation["message"]


@responses.activate
def test_solution_invalid_json_payload2(test_client):
    evaluation = _run_solver(test_client, 200, "[1, 2")
    assert evaluation["score"] == 0
    assert "Error: Failed to parse json <[1, 2>" in evaluation["message"]


@responses.activate
def test_solution_invalid_json_payload3(test_client):
    evaluation = _run_solver(test_client, 200, json.dumps("[1, 2"))
    assert evaluation["score"] == 0
    assert "Error: Expected List[List[int]], got <[1, 2>" in evaluation["message"]


@responses.activate
def test_solution_error_numeric_payload(test_client):
    evaluation = _run_solver(test_client, 200, json.dumps(42))
    assert evaluation["score"] == 0
    assert "Error: Expected List[List[int]], got <42>" in evaluation["message"]


@responses.activate
def test_solution_empty_payload(test_client):
    evaluation = _run_solver(test_client, 200, None)
    assert evaluation["score"] == 0
    assert "Error: Failed to parse json <>" in evaluation["message"]


@responses.activate
def test_solution_empty_string_payload(test_client):
    evaluation = _run_solver(test_client, 200, "")
    assert evaluation["score"] == 0
    assert "Error: Failed to parse json <>" in evaluation["message"]


@responses.activate
def test_solution_empty_string_json_payload(test_client):
    evaluation = _run_solver(test_client, 200, json.dumps(""))
    assert evaluation["score"] == 0
    assert "Error: Expected List[List[int]], got <>" in evaluation["message"]


@responses.activate
def test_solution_empty_list_payload(test_client):
    evaluation = _run_solver(test_client, 200, json.dumps([]))
    assert evaluation["score"] == 0
    assert "Error: Expected 4 results, got 0: []" in evaluation["message"]


@responses.activate
def test_solution_not_enough_results(test_client):
    evaluation = _run_solver(test_client, 200, json.dumps([[], []]))

    assert evaluation["score"] == 0
    assert "Error: Expected 4 results, got 2: [[], []]" in evaluation["message"]


@responses.activate
def test_solution_not_json_mime(test_client):
    context = _EvaluationContext(test_client)
    responses.add(
        responses.POST,
        context.solver_url,
        status=200,
        body="[[11, 13, 20, 23], [], [], []]",
    )
    context.add_evaluate_callback(200)
    evaluate = context.evaluate(use_test_challenge=True)
    body = json.loads(evaluate.request.body.decode("utf-8"))
    assert body["score"] == 5
    assert "Scenario 1 score is 0.45" in body["message"]
    assert "Test run" in body["message"]
    assert "Solver finished in" in body["message"]


@responses.activate
def test_solution(test_client):
    solution = json.dumps([[11, 13, 20, 23], [25, 29], [10, 23, 25], [15, 21, 27, 28]])
    request = _run_solver(test_client, 200, solution, use_test_challenge=True)

    assert request["score"] == 38
    assert ". Scenario 1 score is 0.45" in request["message"]
    assert ". Seed is 3. " in request["message"]


@responses.activate
def test_timeout(test_client):
    context = _EvaluationContext(test_client)
    responses.add(
        responses.POST, context.solver_url, body=requests.exceptions.Timeout()
    )
    context.add_evaluate_callback(200)
    request: requests.PreparedRequest = context.evaluate(
        use_test_challenge=False
    ).request
    request = json.loads(cast(bytes, request.body).decode("utf-8"))
    assert "Error: Timed out after 28s" in request["message"]
    assert request["score"] == 0


# pylint: disable=singleton-comparison
def test_get_bool_value():
    for value in ["True", "TRUE", "true", True]:
        assert app.coerce_to_bool(value, False) == True, value

    for value in ["false", "False", "FALSE", False]:
        assert app.coerce_to_bool(value, True) == False, value

    for value in [None, ""]:
        for default in [True, False]:
            assert app.coerce_to_bool(value, default) == default

    for value in ["hello", 42, "yes", "1", 1, "no", "0", 0]:
        for default in [True, False]:
            with pytest.raises(Exception):
                app.coerce_to_bool(value, default)

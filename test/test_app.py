# pylint: disable=redefined-outer-name,line-too-long

import json
from typing import cast
import pytest
import responses
import requests

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_instructions(client):
    for url in ["/", "/instructions"]:
        response = client.get(url, follow_redirects=True)
        assert b"function family" in response.data
        assert b'class="input"' not in response.data


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


# TODO Delete this method
# pylint: disable=too-many-arguments
def _test_solver_result(
    test_client,
    solver_status_code: int,
    solver_result,
    expected_score: int,
    expected_message: str,
    use_test_challenge: bool = False,
):
    request = _run_solver(
        test_client, solver_status_code, solver_result, use_test_challenge
    )
    assert request["runId"] == "142"
    assert request["score"] == expected_score
    assert request["message"] == expected_message


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
    return json.loads(cast(bytes, request.body).decode("ascii"))


@responses.activate
def test_solution_error(client):
    _test_solver_result(
        client,
        503,
        "Some internal error",
        0,
        "Error: Got 503 from solver https://solver/technical-analysis. Some internal error",
    )


@responses.activate
def test_solution_wrong_format(client):
    _test_solver_result(
        client,
        200,
        "some non-json",
        0,
        "Error: Failed to parse json <some non-json>. Expecting value: line 1 column 1 (char 0)",
    )


# I'm not sure how much state there is in the test_client so doing one test per method


@responses.activate
def test_solution_invalid_json_payload1(client):
    _test_solver_result(
        client,
        200,
        "}",
        0,
        "Error: Failed to parse json <}>. Expecting value: line 1 column 1 (char 0)",
    )


@responses.activate
def test_solution_invalid_json_payload2(client):
    _test_solver_result(
        client,
        200,
        "[1, 2",
        0,
        "Error: Failed to parse json <[1, 2>. Expecting ',' delimiter: line 1 column 6 (char 5)",
    )


@responses.activate
def test_solution_invalid_json_payload3(client):
    _test_solver_result(
        client,
        200,
        json.dumps("[1, 2"),
        0,
        "Error: Expected List[List[int]], got <[1, 2>",
    )


@responses.activate
def test_solution_error_numeric_payload(client):
    _test_solver_result(
        client, 200, json.dumps(42), 0, "Error: Expected List[List[int]], got <42>"
    )


@responses.activate
def test_solution_empty_payload(client):
    _test_solver_result(
        client,
        200,
        None,
        0,
        "Error: Failed to parse json <>. Expecting value: line 1 column 1 (char 0)",
    )


@responses.activate
def test_solution_empty_string_payload(client):
    _test_solver_result(
        client,
        200,
        "",
        0,
        "Error: Failed to parse json <>. Expecting value: line 1 column 1 (char 0)",
    )


@responses.activate
def test_solution_empty_string_json_payload(client):
    _test_solver_result(
        client, 200, json.dumps(""), 0, "Error: Expected List[List[int]], got <>"
    )


@responses.activate
def test_solution_empty_list_payload(client):
    _test_solver_result(
        client, 200, json.dumps([]), 0, "Error: Expected 4 results, got 0: []"
    )


@responses.activate
def test_solution_not_enough_results(client):
    _test_solver_result(
        client,
        200,
        json.dumps([[], []]),
        0,
        "Error: Expected 4 results, got 2: [[], []]",
    )


@responses.activate
def test_solution_not_json_mime(client):
    context = _EvaluationContext(client)
    responses.add(
        responses.POST,
        context.solver_url,
        status=200,
        body="[[11, 13, 20, 23], [], [], []]",
    )
    context.add_evaluate_callback(200)
    evaluate = context.evaluate(use_test_challenge=True)
    body = json.loads(evaluate.request.body.decode("ascii"))
    assert body["score"] == 5
    assert "Scenario 1 score is 0.45" in body["message"]
    assert "Test run" in body["message"]
    assert "Solver finished in" in body["message"]


@responses.activate
def test_solution(client):
    request = _run_solver(
        client,
        200,
        json.dumps(
            [[11, 13, 20, 23], [25, 29], [10, 11, 20, 21, 22, 23, 25], [15, 21, 27, 28]]
        ),
        use_test_challenge=True,
    )

    assert request["score"] == 42
    assert "Scenario 1 score is 0.45" in request["message"]


@responses.activate
def test_timeout(client):
    context = _EvaluationContext(client)
    responses.add(
        responses.POST, context.solver_url, body=requests.exceptions.Timeout()
    )
    context.add_evaluate_callback(200)
    request: requests.PreparedRequest = context.evaluate(
        use_test_challenge=False
    ).request
    request = json.loads(cast(bytes, request.body).decode("ascii"))
    assert (
        request["message"]
        == "Error: https://solver/technical-analysis timed out after 28s"
    )
    assert request["score"] == 0

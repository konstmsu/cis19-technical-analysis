# pylint: disable=redefined-outer-name,line-too-long

import pytest
import responses

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
        assert b"family of functions" in response.data


class _EvaluationContext:
    def __init__(self, test_client):
        self.test_client = test_client
        self.team_url = "https://solver"
        self.evaluate_callback_url = "https://codeit-suisse/evaluate-callback"
        self.solver_response_status = 200

    @property
    def solver_url(self):
        return f"{self.team_url}/technical-analysis"

    def add_solver_response(self, status, json):
        responses.add(responses.POST, self.solver_url, status=status, json=json)

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


# pylint: disable=too-many-arguments
def _test_solver_result(
    test_client,
    solver_status_code: int,
    solver_result,
    expected_score: int,
    expected_message: str,
    use_test_challenge: bool = False,
):
    context = _EvaluationContext(test_client)
    context.add_solver_response(solver_status_code, solver_result)
    context.add_evaluate_callback(200)
    evaluate = context.evaluate(use_test_challenge=use_test_challenge)
    expected_body = f'{{"runId": "142", "score": {expected_score}, "message": "{expected_message}"}}'
    assert evaluate.request.body == expected_body.encode("ascii")


@responses.activate
def test_solution_error(client):
    _test_solver_result(
        client,
        500,
        None,
        0,
        "Error: Got 500 from solver https://solver/technical-analysis",
    )


@responses.activate
def test_solution_wrong_format(client):
    _test_solver_result(
        client,
        200,
        "some non-json",
        0,
        "Error: Expected List[List[int]], got <some non-json>",
    )


# I'm not sure how much state there is in the test_client so doing one test per method


@responses.activate
def test_solution_invalid_json_payload1(client):
    _test_solver_result(client, 200, "}", 0, "Error: Expected List[List[int]], got <}>")


@responses.activate
def test_solution_invalid_json_payload2(client):
    _test_solver_result(
        client, 200, "[1, 2", 0, "Error: Expected List[List[int]], got <[1, 2>"
    )


@responses.activate
def test_solution_error_numeric_payload(client):
    _test_solver_result(client, 200, 42, 0, "Error: Expected List[List[int]], got <42>")


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
def test_solution_numeric_payload(client):
    _test_solver_result(client, 200, "", 0, "Error: Expected List[List[int]], got <>")


@responses.activate
def test_solution_empty_list_payload(client):
    _test_solver_result(client, 200, [], 0, "Error: Expected 4 results, got 0: []")


@responses.activate
def test_solution_not_enough_results(client):
    _test_solver_result(
        client, 200, [[], []], 0, "Error: Expected 4 results, got 2: [[], []]"
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
    expected_body = (
        """{"runId": "142", "score": 5, "message": "Scenario 1 score is 0.45"""
    )
    assert evaluate.request.body.decode("ascii").startswith(expected_body)


@responses.activate
def test_solution(client):
    _test_solver_result(
        client,
        200,
        [[11, 13, 20, 23], [25, 29], [10, 11, 20, 21, 22, 23, 25], [15, 21, 27, 28]],
        42,
        """\
Scenario 1 score is 0.45, amounts are 1.26 / 1.58. \
Scenario 2 score is 1.00, amounts are 1.01 / 1.01. \
Scenario 3 score is 0.13, amounts are 1.05 / 1.37. \
Scenario 4 score is 0.32, amounts are 1.24 / 1.74""",
        use_test_challenge=True,
    )

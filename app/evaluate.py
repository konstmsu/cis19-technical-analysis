from typing import Collection, List
import random
import time
from json import JSONDecodeError

import requests
from flask import request, current_app, Blueprint

from . import generation
from . import trade_optimizer
from . import trade_simulator

BLUEPRINT = Blueprint("evaluate", __name__)

ChallengeInput = List[List[int]]
EvaluateCallbackPayload = dict


@BLUEPRINT.route("/ping")
def test_route():
    return "pong"


@BLUEPRINT.route("/evaluate", methods=["POST"])
def evaluate():
    data: dict = request.get_json()
    team_url = data["teamUrl"]
    callback_url = data["callbackUrl"]
    run_id = data["runId"]
    is_test = data.get("isTest")
    current_app.logger.info(
        f"teamUrl: {team_url}, callbackUrl: {callback_url}, runId: {run_id}, isTest: {is_test}"
    )
    evaluation_result: EvaluateCallbackPayload = execute_team_solution(
        team_url, run_id, is_test
    )

    # pylint: disable=line-too-long
    authorization_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJjb2RlaXRzdWlzc2VhcGFjMjAxOUBnbWFpbC5jb20iLCJleHAiOjE1Njk4NjA2NTF9.l9PrR9r9XFA0gdqvtW1hfOm4bmHSvAVW6es1eV72v3MwjGxBCQPNbE3QtF0WtFKaLEqqaumS8Ut_KkOgG1gWCA"
    callback_result = requests.post(
        callback_url,
        json=evaluation_result,
        headers={"Authorization": authorization_token},
    )

    current_app.logger.info("Evaluate callback returned %s", callback_result.content)

    return {"callback_result": str(callback_result.content)}


def create_challenge_input(scenarios) -> ChallengeInput:
    return [scenario.train_signal.tolist() for scenario in scenarios]


def create_evaluate_callback_response(
    run_id: str, coordinator_score: int, messages: List[str]
) -> EvaluateCallbackPayload:
    return {"runId": run_id, "score": coordinator_score, "message": ". ".join(messages)}


# pylint: disable=too-many-locals
def execute_team_solution(
    team_url: str, run_id: str, is_test: bool
) -> EvaluateCallbackPayload:
    messages = []

    def create_error_response(error):
        messages.append(f"Error: {error}")
        return create_evaluate_callback_response(run_id, 0, messages)

    if is_test:
        messages.append("Test run")

    messages.append(f"runId: {run_id}, teamUrl: {team_url}")

    seed = 3 if is_test else random.randrange(1_000_000_000)
    scenarios = (
        generation.get_standard_scenarios(seed, train_size=10, test_size=20)
        if is_test
        else generation.get_standard_scenarios(seed)
    )

    messages.append(f"Seed is {seed:,}")

    challenge_input: ChallengeInput = create_challenge_input(scenarios)
    solver_url = team_url + "/technical-analysis"
    current_app.logger.info("Posting to %s input %s", solver_url, challenge_input)

    start = time.time()
    timeout = 28
    try:
        response: requests.models.Response = requests.post(
            solver_url, json=challenge_input, timeout=timeout
        )
    except requests.exceptions.Timeout:
        return create_error_response(f"Timed out after {timeout}s")

    end = time.time()
    messages.append(f"Solver finished in {end-start:.1f}s")

    current_app.logger.info("solver_url: %s, response: %s", solver_url, response.text)

    if response.status_code != 200:
        return create_error_response(
            f"Got {response.status_code} from solver {solver_url}. {response.text}"
        )

    try:
        results = response.json()
    except JSONDecodeError as ex:
        return create_error_response(f"Failed to parse json <{response.text}>. {ex}")

    if not isinstance(results, list) or not all(isinstance(r, list) for r in results):
        return create_error_response(f"Expected List[List[int]], got <{results}>")

    try:
        score, score_messages = calculate_coordinator_score(scenarios, results)
        messages += score_messages
        return create_evaluate_callback_response(run_id, score, messages)
    except Exception as ex:  # pylint: disable=broad-except
        return create_error_response(ex)


def calculate_coordinator_score(
    scenarios: Collection[generation.Scenario], results: Collection[Collection[int]]
):
    assert len(results) == len(
        scenarios
    ), f"Expected {len(scenarios)} results, got {len(results)}: {results}"
    messages = []
    scores = []
    for scenario, trades in zip(scenarios, results):
        money = trade_simulator.simulate(
            scenario.test_signal, scenario.train_size, trades
        )

        optimal_trades = [
            scenario.train_size + t
            for t in trade_optimizer.get_optimal_trades(scenario.test_signal)
        ]
        max_money = trade_simulator.simulate(
            scenario.test_signal, scenario.train_size, optimal_trades
        )

        score = trade_simulator.get_score(max_money, money)
        scores.append(score)

        # pylint: disable=line-too-long
        messages.append(
            f"Scenario {scenario.sine_count} score is {score:.2f}, amounts are {money:.2f} / {max_money:.2f}"
        )

    coordinator_score = trade_simulator.get_cooridnator_score(scores)

    return (coordinator_score, messages)

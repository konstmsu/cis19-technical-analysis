from typing import List, Collection, Dict
import random

import requests
from flask import request, current_app, Blueprint, jsonify

from . import generation
from . import trade_optimizer
from . import trade_simulator

BLUEPRINT = Blueprint("evaluate", __name__)

# TODO Utilize TypedDict when Python 3.8 is released
ChallengeInput = List[Dict]


@BLUEPRINT.route("/test")
def test_route():
    return "It Works!"


@BLUEPRINT.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    team_url = data["teamUrl"]
    callback_url = data["callbackUrl"]
    run_id = data["runId"]
    current_app.logger.info(
        f"teamUrl: {team_url}, callbackUrl: {callback_url}, runId: {run_id}"
    )
    score = execute_team_solution(team_url, run_id)

    # pylint: disable=line-too-long
    authorization_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJjb2RlaXRzdWlzc2VhcGFjMjAxOUBnbWFpbC5jb20iLCJleHAiOjE1Njk4NjA2NTF9.l9PrR9r9XFA0gdqvtW1hfOm4bmHSvAVW6es1eV72v3MwjGxBCQPNbE3QtF0WtFKaLEqqaumS8Ut_KkOgG1gWCA"
    callback_result = requests.post(
        callback_url, json=score, headers={"Authorization": authorization_token}
    )

    current_app.logger.info("Evaluate callback returned %s", callback_result.content)

    return jsonify(
        {"evaluate_status": "complete", "callback_result": str(callback_result.content)}
    )


def create_challenge_input(scenarios) -> ChallengeInput:
    return [scenario.train_signal.tolist() for scenario in scenarios]


def execute_team_solution(team_url, run_id):
    scernarios = generation.get_standard_scenarios(random.randrange(1_000_000_000))
    url = team_url + "/technical-analysis"
    challenge_input = create_challenge_input(scernarios)
    current_app.logger.info("Posting to %s input %s", url, challenge_input)
    results = requests.post(url, json=challenge_input).json()
    current_app.logger.info("url: %s, response: %s", url, results)

    return calculate_score(run_id, scernarios, results)


def calculate_score(
    run_id: str,
    scenarios: Collection[generation.Scenario],
    results: Collection[Collection[int]],
):
    assert len(results) == len(scenarios), f"Expected {len(scenarios)} results"
    messages = []
    scores = []
    for scenario, trades in zip(scenarios, results):
        money = trade_simulator.simulate(
            scenario.test_signal, scenario.train_size, trades
        )

        optimal_trades = list(trade_optimizer.get_optimal_trades(scenario.test_signal))
        max_money = trade_simulator.simulate(scenario.test_signal, 0, optimal_trades)

        score = trade_simulator.get_score(max_money, money)
        scores.append(score)

        # pylint: disable=line-too-long
        messages.append(
            f"Scored {score:.2f}. Got money {money:.2f}, max {max_money:.2f}. Optimal trades: {optimal_trades}"
        )

    coordinator_score = trade_simulator.get_cooridnator_score(scores)

    return {"runId": run_id, "score": coordinator_score, "message": "\n".join(messages)}

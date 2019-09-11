from typing import List
import requests
from flask import request, current_app, Blueprint, jsonify

from . import trade_optimizer
from . import trade_simulator
from . import generation

from .generation import ScenarioBuilder

BLUEPRINT = Blueprint("evaluate", __name__)


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


def execute_team_solution(team_url, run_id):
    # TODO Loop over a range of scenarios and get combined score
    # TODO Use random seed
    scernarios = generation.get_standard_scenarios(0)
    challenge_input = [
        {"test_size": s.test_size, "train": s.get_train_price().tolist()}
        for s in scernarios
    ]
    url = team_url + "/technical-analysis"
    current_app.logger.info("Posting to %s input %s", url, challenge_input)
    results = requests.post(url, json=challenge_input).json()
    current_app.logger.info("url: %s, response: %s", url, results)

    return calculate_score(run_id, scernarios, results)


WEIGHTS = [1, 2, 3, 4]


def calculate_score(run_id, scenarios: List[ScenarioBuilder], results):
    total_score = 0
    assert len(WEIGHTS) == len(scenarios)
    messages = []
    for weight, scenario, trades in zip(WEIGHTS, scenarios, results):
        signal = scenario.test_signal
        money = trade_simulator.simulate(signal, trades)

        optimal_trades = list(trade_optimizer.get_optimal_trades(signal))
        max_money = trade_simulator.simulate(signal, optimal_trades)

        score = trade_simulator.get_score(max_money, money)
        total_score += score * weight

        # pylint: disable=line-too-long
        messages.append(
            f"Scored {score:.2f}. Got money {money:.2f}, max {max_money:.2f}. Optimal trades: {optimal_trades}"
        )

    return {"runId": run_id, "score": total_score * 100, "message": "\n".join(messages)}

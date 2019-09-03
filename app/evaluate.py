import requests
import numpy as np
from flask import request, current_app, Blueprint, jsonify

from . import trade_optimizer
from . import trade_simulator
from . import generation

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
    generator = generation.PriceGenerator(42)
    price = generator.generate_price(100)
    challenge_input = {"prices": np.sum(price, axis=0).tolist()}
    url = team_url + "/technical-analysis"
    current_app.logger.info("Posting to %s input %s", url, challenge_input)
    result = requests.post(url, json=challenge_input).json()
    current_app.logger.info("url: %s, response: %s", url, result)

    return calculate_score(run_id, price, result)


def calculate_score(run_id, price, result):
    trades = result["trades"]
    signal = price[0]
    money = trade_simulator.simulate(signal, trades)
    optimal_trades = list(trade_optimizer.get_optimal_trades(signal))
    max_money = trade_simulator.simulate(signal, optimal_trades)

    score = min(100, money / max_money * 100)

    response_message = {}
    response_message["runId"] = run_id
    response_message["score"] = score
    response_message[
        "message"
    ] = f"Got final money {money:.2f} out of {max_money:.2f}. Hence the score is {score:.1f}. Optimal trades were {optimal_trades}"

    return response_message

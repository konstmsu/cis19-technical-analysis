from flask import Blueprint, request, jsonify, current_app
from app.evaluate import ChallengeInput
from . import my_solver

BLUEPRINT = Blueprint("solver", __name__)


@BLUEPRINT.route("/technical-analysis", methods=["POST"])
def solve():
    data: ChallengeInput = request.get_json()
    current_app.logger.info("Input: %s", data)
    result = []
    for scenario in data:
        result.append(my_solver.solve(scenario["train_data"], scenario["test_size"]))
    current_app.logger.info("Output: %s", result)
    return jsonify(result)


@BLUEPRINT.route("/evaluate-callback", methods=["POST"])
def evaluate_callback():
    data = request.get_json()
    current_app.logger.info("Evaluate callback: %s", data)
    return jsonify({"ok": "yes!"})

import time
from flask import Blueprint, request, jsonify, current_app
from app.evaluate import ChallengeInput
from . import my_solver

BLUEPRINT = Blueprint("solver", __name__)


@BLUEPRINT.route("/technical-analysis", methods=["POST"])
def solve():
    print("Sleeping...")
    time.sleep(30)
    challenge_input: ChallengeInput = request.get_json()
    current_app.logger.info("Input: %s", challenge_input)
    result = [
        my_solver.solve(0, train_signal, 1000, 4)[0] for train_signal in challenge_input
    ]
    current_app.logger.info("Output: %s", result)
    return jsonify(result)

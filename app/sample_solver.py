from flask import Blueprint, request, jsonify, current_app, abort
from app.evaluate import ChallengeInput
from . import my_solver

BLUEPRINT = Blueprint("solver", __name__)
ENABLE_SOLVER_KEY = "ENABLE_SOLVER"


@BLUEPRINT.route("/technical-analysis", methods=["POST"])
def solve():
    # pylint: disable=singleton-comparison
    if current_app.config[ENABLE_SOLVER_KEY] != True:
        abort(405)

    challenge_input: ChallengeInput = request.get_json()
    # current_app.logger.info("Input: %s", challenge_input)
    result = [
        my_solver.solve(0, train_signal, 1000, 2)[0] for train_signal in challenge_input
    ]
    # current_app.logger.info("Output: %s", result)
    return jsonify(result)


@BLUEPRINT.route("/evaluate-callback", methods=["POST"])
def evaluate_callback():
    return "test_ok"

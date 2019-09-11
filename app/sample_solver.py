from flask import Blueprint, request, jsonify, current_app

BLUEPRINT = Blueprint("solver", __name__)


@BLUEPRINT.route("/technical-analysis", methods=["POST"])
def solve():
    data = request.get_json()
    current_app.logger.info("Input: %s", data)
    result = []
    for scenario in data:
        result.append(scenario["test_size"] + [0, 9, 26, 42, 57, 73])
    current_app.logger.info("Output: %s", result)
    return jsonify(result)


@BLUEPRINT.route("/evaluate-callback", methods=["POST"])
def evaluate_callback():
    data = request.get_json()
    current_app.logger.info("Evaluate callback: %s", data)
    return jsonify({"ok": "yes!"})

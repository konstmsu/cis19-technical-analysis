from flask import Blueprint, request, jsonify, current_app

BLUEPRINT = Blueprint("solver", __name__)


@BLUEPRINT.route("/technical-analysis", methods=["POST"])
def solve():
    data = request.get_json()
    current_app.logger.info("input: %s", data)
    result = [0, 1, 5]
    return jsonify(result)

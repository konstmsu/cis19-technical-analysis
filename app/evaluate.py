import requests

from flask import request, current_app, Blueprint, jsonify

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
    result = execute_team_solution(team_url)
    score = calculate_score(result, run_id)

    # pylint: disable=line-too-long
    authorization_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJjb2RlaXRzdWlzc2VhcGFjMjAxOUBnbWFpbC5jb20iLCJleHAiOjE1Njk4NjA2NTF9.l9PrR9r9XFA0gdqvtW1hfOm4bmHSvAVW6es1eV72v3MwjGxBCQPNbE3QtF0WtFKaLEqqaumS8Ut_KkOgG1gWCA"
    callback_result = requests.post(
        callback_url, json=score, headers={"Authorization": authorization_token}
    )

    current_app.logger.info("Evaluate callback returned %s", callback_result.content)

    return jsonify(
        {"evaluate_status": "complete", "callback_result": str(callback_result.content)}
    )


def execute_team_solution(team_url):
    challenge_input = {"prices": [500, 501, 520, 518]}
    url = team_url + "/technical-analysis"
    current_app.logger.info("Posting to %s input %s", url, challenge_input)
    response = requests.post(url, json=challenge_input).json()
    current_app.logger.info("url: %s, response: %s", url, response)

    return response


def calculate_score(result, run_id):
    expected_result = 4
    marks_scrored = 0
    message = ""
    if result == expected_result:
        marks_scrored = 100
        message = "Your score " + marks_scrored
    else:
        message = "Failed"

    response_message = {}
    response_message["runId"] = run_id
    response_message["score"] = marks_scrored
    response_message["message"] = message

    return response_message

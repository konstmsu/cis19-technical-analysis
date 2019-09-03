import json
import requests

from flask import request, current_app, Blueprint, jsonify

BLUEPRINT = Blueprint("evaluate", __name__)


@BLUEPRINT.route("/test")
def test_route():
    return "It Works!"


@BLUEPRINT.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    current_app.logger.info(data)
    team_url = data["teamUrl"]
    callback_url = data["callbackUrl"]
    run_id = data["runId"]
    current_app.logger.info(
        f"teamUrl: {team_url}, callbackUrl: {callback_url}, runId: {run_id}"
    )
    result = execute_team_solution(team_url)
    return_message = calculate_score(result, run_id)

    url_substring = callback_url.split("://")
    secure_url = url_substring[0] + "://cisadmin:soltandpepper@" + url_substring[1]
    requests.post(secure_url, data=return_message)
    return jsonify({"evaluate_status": "complete"})


def execute_team_solution(team_url):
    test_data = {}
    test_data["input"] = 2
    test_data_json = json.dumps(test_data)
    url = team_url + "/challenge"
    response_content = str(requests.post(url, data=test_data_json).content, "utf-8")
    current_app.logger.info("teamUrl: " + team_url + "team result: " + response_content)

    return response_content


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

    return json.dumps(response_message)

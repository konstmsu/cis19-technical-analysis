import json
import logging
import requests

from flask import request, current_app, Blueprint, jsonify

BLUEPRINT = Blueprint("evaluate", __name__)


@BLUEPRINT.route("/test")
def test_route():
    return "It Works!"


@BLUEPRINT.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    current_app.logger.warn(data)
    teamUrl = data["teamUrl"]
    callbackUrl = data["callbackUrl"]
    runId = data["runId"]
    current_app.logger.info(
        f"teamUrl: {teamUrl}, callbackUrl: {callbackUrl}, runId: {runId}"
    )
    result = execute_team_solution(teamUrl)
    returnMessage = calculate_score(result, runId)

    urlSubstring = callbackUrl.split("://")
    secureUrl = urlSubstring[0] + "://cisadmin:soltandpepper@" + urlSubstring[1]
    requests.post(secureUrl, data=returnMessage)
    return jsonify({"evaluate_status": "complete"})


def execute_team_solution(teamUrl):
    testData = {}
    testData["input"] = 2
    json_testData = json.dumps(testData)
    url = teamUrl + "/challenge"
    response_content = str(requests.post(url, data=json_testData).content, "utf-8")
    current_app.logger.info("teamUrl: " + teamUrl + "team result: " + response_content)

    return response_content


def calculate_score(result, runId):
    expectedResult = 4
    marksScrored = 0
    message = ""
    if result == expectedResult:
        marksScrored = 100
        message = "Your score " + marksScrored
    else:
        message = "Failed"

    responseMessage = {}
    responseMessage["runId"] = runId
    responseMessage["score"] = marksScrored
    responseMessage["message"] = message

    return json.dumps(responseMessage)

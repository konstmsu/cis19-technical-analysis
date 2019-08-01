import json
import logging
import requests

from flask import request;
from challenge import app;

logger = logging.getLogger(__name__)
@app.route('/test')
def test_route():
    return "It Works!"

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json();
    teamUrl = data.get("teamUrl");
    callbackUrl = data.get("callbackUrl");
    runId = data.get("runId")
    logging.info('teamUrl:' + teamUrl + '- callbackUrl:' + callbackUrl + '- runId:' + runId)
    result = execute_team_solution(teamUrl);
    returnMessage = calculate_score(result, runId);

    urlSubstring = callbackUrl.split('://');
    secureUrl = urlSubstring[0] + '://cisadmin:soltandpepper@' + urlSubstring[1];
    requests.post(secureUrl, data=returnMessage);


def execute_team_solution(teamUrl):
    testData = {};
    testData['input'] = 2;
    json_testData = json.dumps(testData);
    url = teamUrl + '/challenge';
    response = requests.post(url, data=json_testData);
    logger.info('teamUrl: ' + teamUrl + 'team result: ' + response.content)

    return response.content


def calculate_score(result, runId):
    expectedResult = 4;
    marksScrored = 0;
    message = '';
    if result == expectedResult:
        marksScrored = 100;
        message = 'Your score ' + marksScrored;
    else:
        message = "Failed";

    responseMessage = {};
    responseMessage['runId'] = runId;
    responseMessage['score'] = marksScrored;
    responseMessage['message'] = message;

    json_responseMessage = json.dumps(responseMessage);
    return json_responseMessage;




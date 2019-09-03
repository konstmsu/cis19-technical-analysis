# pylint: disable=redefined-outer-name

import responses

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_instructions(client):
    for url in ["/", "/instructions"]:
        response = client.get(url, follow_redirects=True)
        assert b"Build trading strategy" in response.data


@responses.activate
def test_evaluate(client):
    responses.add(
        responses.POST,
        "http://solver/challenge",
        json={"error": "not found"},
        status=404,
    )

    responses.add(
        responses.POST,
        "http://cisadmin:soltandpepper@codeit-suisse/result",
        json={"error": "not found"},
        status=404,
    )

    response = client.post(
        "/evaluate",
        json={
            "teamUrl": "http://solver",
            "callbackUrl": "http://codeit-suisse/result",
            "runId": "142",
        },
    )

    assert response.status == "200 OK"
    assert response.get_json() == {"evaluate_status": "complete"}

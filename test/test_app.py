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
        "https://solver/technical-analysis",
        json={"error": "not found"},
        status=404,
    )

    responses.add(
        responses.POST,
        "https://codeit-suisse/result",
        json={"error": "not found"},
        status=200,
    )

    response = client.post(
        "/evaluate",
        json={
            "teamUrl": "https://solver",
            "callbackUrl": "https://codeit-suisse/result",
            "runId": "142",
        },
    )

    assert response.status == "200 OK"
    assert response.get_json() == {"evaluate_status": "complete"}

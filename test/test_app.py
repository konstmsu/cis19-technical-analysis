# pylint: disable=redefined-outer-name

import pytest
import responses

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
        json=[[100, 120], [205, 210, 215], [], []],
        status=200,
    )

    responses.add(
        responses.POST, "https://codeit-suisse/evaluate-callback", body="ok", status=200
    )

    response = client.post(
        "/evaluate",
        json={
            "teamUrl": "https://solver",
            "callbackUrl": "https://codeit-suisse/evaluate-callback",
            "runId": "142",
        },
    )

    assert response.status == "200 OK"
    assert response.get_json() == {
        "evaluate_status": "complete",
        "callback_result": "b'ok'",
    }

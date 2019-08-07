import os
import tempfile
import responses

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_instructions(client):
    for url in ["/", "/instructions"]:
        rv = client.get(url, follow_redirects=True)
        assert b"Build trading strategy" in rv.data


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

    client.post(
        "/evaluate",
        json={
            "teamUrl": "http://solver",
            "callbackUrl": "http://codeit-suisse/result",
            "runId": "142",
        },
    )

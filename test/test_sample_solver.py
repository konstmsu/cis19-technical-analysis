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


@responses.activate
def test_evaluate(client):
    response = client.post(
        "/technical-analysis", json=[list(range(20 + i)) for i in range(4)]
    )

    assert response.status == "200 OK"
    assert response.get_json() == [[20 + i, 1019 + i] for i in range(4)]

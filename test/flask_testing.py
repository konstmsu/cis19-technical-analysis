import pytest
from app import create_app


@pytest.fixture
def test_client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        client.app = app
        yield client

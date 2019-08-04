import os
import tempfile

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_root_redirect(client):
    rv = client.get('/')
    assert rv.status_code == 302


def test_instructions(client):
    rv = client.get('/instructions')
    assert b'Build trading strategy' in rv.data

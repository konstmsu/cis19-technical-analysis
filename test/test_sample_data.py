# pylint: disable=redefined-outer-name,unused-import
from test.flask_testing import test_client
import os
import zipfile
import json
import numpy as np


def test_get_sample_data(test_client):
    response = test_client.get("/static/sample_data.zip")
    headers = response.headers
    assert b"HTML" not in response.data
    assert "zip" in headers["Content-Type"]
    assert 500_000 < int(headers["Content-Length"]) < 600_000
    assert headers["Content-Disposition"] == "attachment; filename=sample_data.zip"


def test_readme_in_zip():
    with zipfile.ZipFile("./static/sample_data.zip", "r") as zip_file:
        readme = zip_file.read("README.TXT").decode("utf-8")
        assert "Technical Analysis" in readme
        assert "CodeIT Suisse 2019" in readme


def test_json_in_zip():
    with zipfile.ZipFile("./static/sample_data.zip", "r") as zip_file:
        training_signal = np.asarray(json.loads(zip_file.read("TA_100.json")))

    assert training_signal.shape[0] == 4
    assert training_signal.shape[1] == 100
    for price in training_signal.ravel():
        assert 200 < price < 400

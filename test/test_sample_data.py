# pylint: disable=redefined-outer-name,unused-import
from test.flask_testing import test_client


def test_sample_data(test_client):
    response = test_client.get("/technical_analysis_sample_data.zip")
    headers = response.headers
    assert b"HTML" not in response.data
    assert headers["Content-Type"] == "application/zip"
    assert headers["Content-Length"] == "539346"
    assert (
        headers["Content-Disposition"]
        == "attachment; filename=technical_analysis_sample_data.zip"
    )

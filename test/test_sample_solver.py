# pylint: disable=redefined-outer-name,unused-import

from test.flask_testing import test_client
import responses


@responses.activate
def test_evaluate(test_client):
    response = test_client.post(
        "/technical-analysis", json=[list(range(20 + i)) for i in range(4)]
    )

    assert response.status == "200 OK"
    assert response.get_json() == [[20 + i, 1019 + i] for i in range(4)]

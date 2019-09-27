# pylint: disable=redefined-outer-name,unused-import

from test.flask_testing import test_client
import responses
import numpy as np
from app.generation import get_standard_scenarios
from app.sample_solver import ENABLE_SOLVER_KEY


@responses.activate
def test_evaluate(test_client):
    test_client.app.config[ENABLE_SOLVER_KEY] = True

    def curvy(indexes):
        return np.sin(indexes * 0.005) + indexes

    response = test_client.post(
        "/technical-analysis",
        json=[curvy(np.arange(100 + i)).tolist() for i in range(4)],
    )

    assert response.status == "200 OK"
    assert response.get_json() == [[100 + i, 1099 + i] for i in range(4)]

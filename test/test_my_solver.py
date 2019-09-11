import test.my_solver
import numpy as np
from app import generation, trade_simulator


def test_my_solver():
    scenario = list(generation.get_standard_scenarios(0))[0]
    trades = np.array(
        test.my_solver.solve(scenario.get_train_price(), scenario.test_size)
    )
    result = trade_simulator.simulate(scenario.test_signal, trades)
    # TODO Solver should score better
    assert result > 0.5

from app import my_solver
import numpy as np
from app import generation, trade_simulator


def test_my_solver():
    scenario = list(generation.get_standard_scenarios(0))[0]
    trades = my_solver.solve(scenario.get_train_price(), scenario.test_size)
    result = trade_simulator.simulate(scenario.test_signal, scenario.train_size, trades)
    assert result > 1.5

from app import generation, trade_simulator
from app import my_solver
from app.trade_optimizer import get_optimal_trades


def test_my_solver():
    for seed in range(10):
        for scenario_index, scenario in enumerate(
            generation.get_standard_scenarios(seed)
        ):
            trades, _, _ = my_solver.solve(
                scenario.get_train_price(), scenario.test_size
            )
            result = trade_simulator.simulate(
                scenario.test_signal, scenario.train_size, trades
            )
            optimal_trades = list(get_optimal_trades(scenario.test_signal))
            max_result = trade_simulator.simulate(
                scenario.test_signal, 0, optimal_trades
            )
            assert result == max_result, f"Seed {seed}, scenario {scenario_index}"

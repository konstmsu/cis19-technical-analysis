from app import generation, trade_simulator
from app import my_solver
from app.trade_optimizer import get_optimal_trades


def test_my_solver():
    for seed in range(1, 3):
        for scenario_index, scenario in enumerate(
            generation.get_standard_scenarios(seed)
        ):
            trades, _, _ = my_solver.solve(
                0, scenario.train_signal, scenario.test_size, scenario.sine_count
            )
            result = trade_simulator.simulate(
                scenario.test_signal, scenario.train_size, trades
            )
            optimal_trades = list(get_optimal_trades(scenario.test_signal))
            max_result = trade_simulator.simulate(
                scenario.test_signal, 0, optimal_trades
            )
            quality = result / max_result
            # pylint: disable=line-too-long
            assert (
                0.93 <= quality <= 1
            ), f"Seed {seed}, scenario {scenario_index}, result {result:.2f}, max {max_result:.2f}, model_parameters {scenario.model_parameters}"

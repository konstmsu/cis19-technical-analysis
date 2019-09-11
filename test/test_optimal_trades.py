import glob
import json
from test import my_solver
import numpy as np
from app.trade_optimizer import get_optimal_trades
from app.generation import get_standard_scenarios
from app.trade_simulator import simulate, get_score


def do_test(values, expected_optimal_trades):
    assert list(get_optimal_trades(values)) == expected_optimal_trades


def test_increasing():
    do_test([1, 2], [0, 1])
    do_test([3, 7, 8, 9], [0, 3])


def test_decreasing():
    do_test([5, 3], [])
    do_test([7, 5, 3], [])


def test_peak():
    do_test([5, 3, 4], [1, 2])
    do_test([2, 7, 9, 4], [0, 2])


def test_files(snapshot):
    price_inputs = glob.glob("test/price_*.json")
    assert price_inputs
    for i in price_inputs:
        with open(i) as file:
            data = np.asarray(json.load(file))
        trades = list(get_optimal_trades(data[0]))
        snapshot.assert_match(trades)


# pylint: disable=cell-var-from-loop
def test_brute():
    scores = {}
    for seed in range(100):
        for i, scenario in enumerate(get_standard_scenarios(seed)):

            signal = scenario.test_signal

            optimal_trades = list(get_optimal_trades(signal))
            optimal_result = simulate(signal, optimal_trades)

            description = f"Seed {seed}, scenario {i}"

            def record(name, trades, score_assertion):
                result = simulate(signal, trades)
                score = get_score(optimal_result, result)
                assert score_assertion(score), description
                scores.setdefault(f"{name}_{i}", []).append(score)

            record("empty", [], lambda s: s == 0)
            record("all", range(len(signal)), lambda s: s < 0.2)
            record(
                "random",
                np.random.RandomState(seed).randint(
                    scenario.test_size, size=len(optimal_trades)
                ),
                lambda s: s < 0.2,
            )
            # TODO Solver should be better scoring
            record(
                "my solver",
                my_solver.solve(scenario.get_train_price(), scenario.test_size),
                lambda s: s >= 0,
            )

    for k in sorted(scores.keys()):
        print(f"{k} max is {max(scores[k]):.3f}")

    # assert 1 == 2

import glob
import json

import numpy as np

from app.generation import get_standard_scenarios
from app.trade_optimizer import get_optimal_trades
from app import evaluate


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
    for seed in range(100):
        scenarios = get_standard_scenarios(seed)

        def test(name, results):
            coordinator_score, _ = evaluate.calculate_coordinator_score(
                scenarios, results
            )
            assert coordinator_score < 5, f"{name} brute, seed {seed}"

        test("empty", [[] for _ in scenarios])
        test("all", [np.arange(s.test_size) + s.train_size for s in scenarios])
        rnd = np.random.RandomState(seed)
        test(
            "random",
            [
                rnd.randint(
                    s.train_size, s.size, size=int(2 * sum(s.model_parameters[3::2]))
                )
                for s in scenarios
            ],
        )

    # assert 1 == 2

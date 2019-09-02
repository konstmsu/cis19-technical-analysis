import glob
import json
import numpy as np
from app.trade_optimizer import get_optimal_trades
from app.generation import PriceGenerator
from app.trade_simulator import simulate


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


def test_brute():
    generator = PriceGenerator()
    price = generator.generate_price(100)[0]
    all_result = simulate(price, range(len(price)))
    optimal_result = simulate(price, get_optimal_trades(price))
    print(f"All is {all_result}, optimal is {optimal_result}")
    assert all_result < optimal_result / 7

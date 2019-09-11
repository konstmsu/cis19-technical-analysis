import pytest
from app.trade_simulator import simulate


def test_simple():
    assert simulate([10, 15], []) == 1.0


def test_buy_low_sell_high():
    assert simulate([10, 20], [0, 1]) == 2.0


def test_buy_high_sell_low():
    assert simulate([15, 10, 9], [1, 2]) == 0.9


def test_last_trade_was_buy():
    assert simulate([10, 15, 4], [0, 1, 2]) == 1.5


def test_always_sell_at_the_end():
    assert simulate([10, 15], [0]) == 1.5


def test_sort_trades():
    assert simulate([20, 10], [1, 0]) == 0.5


def test_out_of_range():
    with pytest.raises(Exception, match=r"-1 is out of range"):
        simulate([42], [-1])

    with pytest.raises(Exception, match=r"1 is out of range"):
        simulate([42], [1])

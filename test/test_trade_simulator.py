import pytest
import numpy as np
from app.trade_simulator import simulate


def test_simple():
    assert simulate([10, 15], 0, []) == 1.0


def test_buy_low_sell_high():
    assert simulate([10, 20], 0, [0, 1]) == 2.0


def test_buy_high_sell_low():
    assert simulate([15, 10, 9], 0, [1, 2]) == 0.9


def test_last_trade_was_buy():
    assert simulate([10, 15, 4], 0, [0, 1, 2]) == 1.5


def test_always_sell_at_the_end():
    assert simulate([10, 15], 0, [0]) == 1.5


def test_sort_trades():
    assert simulate([20, 10], 0, [1, 0]) == 0.5


def test_trade_zero():
    assert simulate([10, 20], 300, [300, 301]) == 2.0


def test_out_of_range():
    with pytest.raises(Exception, match=r"Trade -1 must be in \[0, 1\)"):
        simulate([42], 0, [-1])

    with pytest.raises(Exception, match=r"Trade 2 must be in \[0, 2\)"):
        simulate([42, 43], 0, [2])

    with pytest.raises(Exception, match=r"Trade 9 must be in \[10, 11\)"):
        simulate([42], 10, [9])

    with pytest.raises(Exception, match=r"Trade 11 must be in \[100, 102\)"):
        simulate([42, 43], 100, [11])

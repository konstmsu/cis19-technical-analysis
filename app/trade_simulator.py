from typing import Collection
import math

import numpy as np


def simulate(signal: np.ndarray, zero_trade: int, trades: Collection[int]):
    signal = np.asarray(signal)
    trades = list(trades)

    upper_bound = zero_trade + signal.shape[0]

    for trade in trades:
        if not zero_trade <= trade < upper_bound:
            raise Exception(f"Trade {trade} must be in [{zero_trade}, {upper_bound})")

    money = 1
    security = 0

    for trade in sorted(trades):
        price = signal[trade - zero_trade]
        if security:
            money = price * security
            security = 0
        else:
            security = money / price
            money = 0

    if security:
        money = signal[-1] * security

    return money


def get_score(optimal_result, result):
    return min(1, max(0, (result - 1) / (optimal_result - 1)))


def get_cooridnator_score(scores) -> int:
    weights = np.asarray([1, 2, 3, 4])
    scores = np.clip(np.asarray(scores), 0, 1)
    return int(math.ceil(100 / sum(weights) * np.sum(scores * weights)))

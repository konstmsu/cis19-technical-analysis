from typing import Collection

import numpy as np


def simulate(signal: np.ndarray, zero_trade: int, trades: Collection[int]):
    if trades:
        upper_bound = zero_trade + len(signal)

        for trade in trades:
            if not zero_trade <= trade < upper_bound:
                raise Exception(
                    f"Trade {trade} must be in [{zero_trade}, {upper_bound})"
                )

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

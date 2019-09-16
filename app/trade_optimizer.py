from typing import Iterable

import numpy as np


def get_optimal_trades(signal: np.ndarray) -> Iterable[int]:
    diffs = np.diff(signal)
    is_next_min = True
    for i, diff in enumerate(diffs):
        if (is_next_min and diff > 0) or (not is_next_min and diff < 0):
            yield i
            is_next_min = not is_next_min

    if not is_next_min and diffs[-1] > 0:
        yield len(diffs)

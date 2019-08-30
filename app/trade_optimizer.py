import typing
import numpy as np


def get_optimal_trades(values: np.ndarray) -> typing.Generator[int, None, None]:
    diffs = np.diff(values)
    is_next_min = True
    for i, diff in enumerate(diffs):
        if (is_next_min and diff > 0) or (not is_next_min and diff < 0):
            yield i
            is_next_min = not is_next_min

    if not is_next_min and diffs[-1] > 0:
        yield len(diffs)

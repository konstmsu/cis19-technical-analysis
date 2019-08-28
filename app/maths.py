import numpy as np
import typing


def optimal_trades(values: np.ndarray) -> typing.Generator[int, None, None]:
    diff = np.diff(values)
    isLookingForMin = True
    for i in range(len(diff)):
        if (isLookingForMin and diff[i] > 0) or (not isLookingForMin and diff[i] < 0):
            yield i
            isLookingForMin = not isLookingForMin

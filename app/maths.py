import numpy as np


def local_extrema(values):
    diff = np.sign(np.diff(values))
    return np.argwhere(diff != 0)

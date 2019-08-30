import operator
from functools import reduce
import numpy as np


def get_trend(size):
    return np.arange(size) / (size - 1)


def get_saw(size, period_length):
    return np.mod(np.arange(size), period_length) / (period_length - 1)


def get_wave(size, period_length):
    return 0.5 + 0.5 * np.sin(2 * np.pi / period_length * np.arange(size))


def get_waves(size, period_lengths):
    components = (get_wave(size, l) for l in period_lengths)
    return reduce(operator.add, components, np.zeros(size))


# pylint: disable=too-few-public-methods
class PriceGenerator:
    def __init__(self, random_seed=None):
        self.random_seed = random_seed

    def generate_price(self, size: int):
        rnd = np.random.RandomState(self.random_seed)
        # TODO Add offset to avoid zero sines @ 0
        signal = np.ones(size)
        signal += 1 * get_waves(size, [size // 3])
        # signal += 1 * get_saw(size, size // 5)
        # signal += 1 * get_trend(size)
        noise = 0.01 * rnd.randn(size)
        return np.stack((signal, noise))

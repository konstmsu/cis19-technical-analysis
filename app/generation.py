import numpy as np
from functools import reduce
import operator


def get_trend(n):
    return np.arange(n) / (n - 1)


def get_saw(n, period_length):
    return np.mod(np.arange(n), period_length) / (period_length - 1)


def get_wave(n, period_length):
    return 0.5 + 0.5 * np.sin(2 * np.pi / period_length * np.arange(n))


def get_waves(n, period_lengths):
    components = (get_wave(n, l) for l in period_lengths)
    return reduce(operator.add, components, np.zeros(n))


class PriceGenerator:
    def __init__(self, random_seed=None):
        self.random_seed = random_seed

    def generate_price(self, n: int):
        rnd = np.random.RandomState(self.random_seed)
        # TODO Add offset to avoid zero sines @ 0
        signal = np.ones(n)
        signal += 1 * get_waves(n, [n // 3])
        # signal += 1 * get_saw(n, n // 5)
        # signal += 1 * get_trend(n)
        noise = 0.01 * rnd.randn(n)
        return np.stack((signal, noise))

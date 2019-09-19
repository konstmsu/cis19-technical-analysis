from typing import List

import numpy as np


def base(size: int) -> np.ndarray:
    return np.ones(size)


def trend(size: int) -> np.ndarray:
    return np.linspace(0, 1, size)


def saw(size: int, period_count: float):
    return np.mod(np.linspace(0, period_count, size), 1)


def wave(size: int, period_count: float) -> np.ndarray:
    return np.sin(np.linspace(0, 2 * np.pi * period_count, size))


# pylint: disable=too-many-instance-attributes
class ScenarioBuilder:
    def __init__(self, random_seed: int, train_size: int, test_size: int):
        self.rnd = np.random.RandomState(random_seed)
        self.test_size = test_size

        self.train_noise = np.zeros(train_size)

        self.signal_description: List[str] = []
        self.signal = np.zeros(train_size + test_size)
        self.train_signal = self.signal[:train_size]
        self.test_signal = self.signal[train_size:]
        self.wave_count = 1

    @property
    def train_size(self):
        return self.train_signal.shape[0]

    @property
    def size(self):
        return self.train_size + self.test_size

    def _add(self, description: str, signal: np.ndarray):
        self.signal_description.append(description)
        self.signal += signal

    def add_base(self):
        scale = self.rnd.uniform(200, 300)
        self._add(f"{scale:.0f}", scale * base(self.size))
        return self

    def add_trend(self):
        scale = self.rnd.uniform(-100, 100)
        self._add(f"trend[{scale:.0f}]", scale * trend(self.size))
        return self

    def create_period_counts(self, count):
        for _ in range(100):
            period_counts = np.sort(self.rnd.uniform(20, 50, count))
            if count < 2 or min(np.diff(period_counts)) > 5:
                return period_counts
        return period_counts

    def add_waves(self, count: int):
        self.wave_count += count
        scales = self.rnd.uniform(5, 15, count)
        period_counts = self.create_period_counts(count)

        for scale, period_count in zip(scales, period_counts):
            self._add(
                f"{period_count:.1f} sines sized {scale:.0f}",
                scale * wave(self.size, period_count),
            )
        return self

    def add_noise(self):
        # self.train_noise += self.rnd.standard_normal(self.train_size)
        # self.signal_description.append("noise")
        return self

    def get_train_price(self) -> np.ndarray:
        return self.train_signal + self.train_noise


def get_standard_scenarios(random_seed: int) -> List[ScenarioBuilder]:
    rnd = np.random.RandomState(random_seed)

    def next_seed():
        return rnd.randint(2 ** 32 - 1)

    def create_builder(train_size, test_size):
        return (
            ScenarioBuilder(next_seed(), train_size, test_size).add_base().add_trend()
        )

    def get_satisfactory(train_size, test_size, builder_func):
        for attempt in range(10):
            builder = builder_func(create_builder(train_size, test_size))
            if min(builder.signal) > 0 and min(builder.get_train_price()) > 0:
                return builder
            print(f"Attempt {attempt} failed")

        raise Exception("couldn't create satisfactory scenario")

    return [
        get_satisfactory(100, 1000, lambda b: b.add_waves(1)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(2)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(3)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(4)),
    ]

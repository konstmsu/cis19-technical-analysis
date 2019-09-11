from typing import List
import numpy as np


def base(size: int) -> np.ndarray:
    return np.ones(size)


def trend(size: int) -> np.ndarray:
    return np.linspace(0, 1, size)


def saw(size: int, period_count: float):
    return np.mod(np.linspace(0, period_count, size), 1)


def wave(size: int, offset: float, period_count: float) -> np.ndarray:
    return 0.5 + 0.5 * np.sin(offset + np.linspace(0, 2 * np.pi * period_count, size))


class ScenarioBuilder:
    def __init__(self, random_seed: int, train_size: int, test_size: int):
        self.train_size = train_size
        self.test_size = test_size
        self.size = train_size + test_size

        self.signal = np.zeros(self.size)
        self.signal_description: List[str] = []
        self.noise = np.zeros(self.size)
        self.rnd = np.random.RandomState(random_seed)

        self.train_signal = self.signal[:train_size]
        self.test_signal = self.signal[train_size:]
        self.train_noise = self.noise[:train_size]

    def _add(self, description: str, signal: np.ndarray):
        self.signal_description.append(description)
        self.signal += signal

    def add_base(self):
        scale = self.rnd.uniform(200, 300)
        self._add("base", scale * base(self.size))
        return self

    def add_trend(self):
        scale = self.rnd.uniform(-100, 100)
        self._add("trend", scale * trend(self.size))
        return self

    def add_waves(self, count: int):
        scales = self.rnd.uniform(5, 15, count)
        period_counts = self.rnd.uniform(20, 50, count)
        offset = self.rnd.uniform(0, self.size * 10)
        for scale, period_count in zip(scales, period_counts):
            self._add(f"wave", scale * wave(self.size, offset, period_count))
        return self

    def add_noise(self):
        self.noise += self.rnd.standard_normal(self.size)
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
            if min(builder.signal) > 0 and min(builder.signal + builder.noise) > 0:
                return builder
            print(f"Attempt {attempt} failed")

        raise Exception("couldn't create satisfactory scenario")

    return [
        get_satisfactory(100, 1000, lambda b: b.add_waves(1)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(3)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(6).add_noise()),
        get_satisfactory(100, 1000, lambda b: b.add_waves(20).add_noise()),
    ]

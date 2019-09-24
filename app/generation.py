from typing import List
import numpy as np


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Scenario:
    def __init__(self, model, model_parameters, train_size: int, test_size: int):
        self.model_parameters = model_parameters
        self.model = model

        signal = model(np.arange(train_size + test_size), *model_parameters)

        # intentional loss of precision on train signal
        self.train_signal = signal[:train_size].astype(np.int32, casting="unsafe")
        self.test_signal = signal[-test_size:]

        assert self.train_signal.shape[0] + self.test_signal.shape[0] == self.size

    @property
    def sine_count(self):
        return (len(self.model_parameters) - 2) // 2

    @property
    def train_size(self):
        return self.train_signal.shape[0]

    @property
    def test_size(self):
        return self.test_signal.shape[0]

    @property
    def size(self):
        return self.train_size + self.test_size


class ScenarioBuilder:
    def __init__(self, random_seed: int, train_size: int, test_size: int):
        self.rnd = np.random.RandomState(random_seed)
        self.train_size = train_size
        self.test_size = test_size
        self.model_parameters = np.array([0, 0])

    def build(self) -> Scenario:
        x_scale = 1 / (self.train_size + self.test_size - 1)
        # pylint: disable=invalid-name
        def model(x, base, trend, *waves):
            result = base + trend * x_scale * x

            for scale, period_count in zip(waves[::2], waves[1::2]):
                result += scale * np.sin(2 * np.pi * period_count * x_scale * x)

            return result

        return Scenario(model, self.model_parameters, self.train_size, self.test_size)

    def set_base(self, rng=(200, 300)):
        self.model_parameters[0] = self.rnd.uniform(rng[0], rng[1])
        return self

    def set_trend(self, rng=(-100, 100)):
        self.model_parameters[1] = self.rnd.uniform(rng[0], rng[1])
        return self

    def _create_period_counts(self, count, period_count_range):
        for _ in range(100):
            low, high = period_count_range
            period_counts = np.sort(self.rnd.uniform(low, high, count))
            if count < 2 or min(np.diff(period_counts)) > low:
                return period_counts
        raise Exception(
            f"Could not come up with {count} periods in range ({low}, {high})"
        )

    def add_waves(self, count: int, scale_range=(5, 15), period_count_range=(10, 100)):
        scales = self.rnd.uniform(scale_range[0], scale_range[1], count)
        period_counts = self._create_period_counts(count, period_count_range)

        for scale, period_count in zip(scales, period_counts):
            self.model_parameters = np.append(
                self.model_parameters, [scale, period_count]
            )

        return self


def get_standard_scenarios(
    random_seed: int, train_size: int = 100, test_size: int = 1000
) -> List[Scenario]:
    rnd = np.random.RandomState(random_seed)

    def next_seed():
        return rnd.randint(1_000_000_000)

    def create_builder(train_size, test_size):
        return (
            ScenarioBuilder(next_seed(), train_size, test_size).set_base().set_trend()
        )

    def get_satisfactory(train_size, test_size, builder_func):
        for attempt in range(10):
            builder = builder_func(create_builder(train_size, test_size))
            scenario = builder.build()
            if min(scenario.train_signal) > 0 and min(scenario.test_signal) > 0:
                return scenario
            print(f"Attempt {attempt} failed")

        raise Exception("couldn't create satisfactory scenario")

    return [
        get_satisfactory(train_size, test_size, lambda b: b.add_waves(1)),
        get_satisfactory(train_size, test_size, lambda b: b.add_waves(2)),
        get_satisfactory(train_size, test_size, lambda b: b.add_waves(3)),
        get_satisfactory(train_size, test_size, lambda b: b.add_waves(4)),
    ]

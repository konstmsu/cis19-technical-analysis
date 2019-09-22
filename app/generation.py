from typing import List
import numpy as np


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Scenario:
    def __init__(self, model, model_parameters, train_size: int, test_size: int):
        self.train_size = train_size
        self.test_size = test_size
        self.size = train_size + test_size

        self.model_parameters = model_parameters
        self.model = model

        signal = model(np.arange(self.size), *model_parameters)
        self.train_signal = np.round(signal[:train_size]).astype(
            np.int32, casting="unsafe"
        )
        self.test_signal = signal[-test_size:]

        assert self.train_signal.shape[0] + self.test_signal.shape[0] == self.size

    @property
    def sine_count(self):
        return (len(self.model_parameters) - 2) // 2


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

    def set_base(self):
        self.model_parameters[0] = self.rnd.uniform(200, 300)
        return self

    def set_trend(self):
        self.model_parameters[1] = self.rnd.uniform(-100, 100)
        return self

    def _create_period_counts(self, count):
        for _ in range(100):
            period_counts = np.sort(self.rnd.uniform(11, 100, count))
            if count < 2 or min(np.diff(period_counts)) > 10:
                return period_counts
        raise Exception(f"Could not come up with {count} periods")

    def add_waves(self, count: int):
        scales = self.rnd.uniform(5, 15, count)
        period_counts = self._create_period_counts(count)

        for scale, period_count in zip(scales, period_counts):
            self.model_parameters = np.append(
                self.model_parameters, [scale, period_count]
            )

        return self


def get_standard_scenarios(random_seed: int) -> List[Scenario]:
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
        get_satisfactory(100, 1000, lambda b: b.add_waves(1)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(2)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(3)),
        get_satisfactory(100, 1000, lambda b: b.add_waves(4)),
    ]

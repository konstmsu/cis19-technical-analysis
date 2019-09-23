from typing import Tuple, List, Callable, Dict

import numpy as np
from scipy.optimize import curve_fit, differential_evolution

from app.trade_optimizer import get_optimal_trades


def solve(
    random_seed: int, train_signal: np.ndarray, test_size: int, max_wave_count: int
) -> Tuple[List[int], Callable[[np.ndarray], np.ndarray], Dict]:
    train_signal = np.asarray(train_signal).astype(np.float32)
    train_size = train_signal.shape[0]
    train_x = np.arange(train_size)
    size = train_size + test_size

    x_scale = 1 / (size - 1)

    # pylint: disable=invalid-name
    def model(x, base, trend, *waves):
        result = base + trend * x_scale * x

        for scale, period_count in zip(waves[::2], waves[1::2]):
            result += scale * np.sin(2 * np.pi * period_count * x_scale * x)

        return result

    def generate_initial_parameters():
        def model_error(model_parameters):
            return np.sum((train_signal - model(train_x, *model_parameters)) ** 2.0)

        parameter_bounds = []
        parameter_bounds.append([200, 300])
        parameter_bounds.append([-100, 100])
        for _ in range(max_wave_count):
            parameter_bounds.append([0, 15])
            parameter_bounds.append([10, 100])

        result = differential_evolution(model_error, parameter_bounds, seed=random_seed)
        return result.x

    popt, _ = curve_fit(model, train_x, train_signal, p0=generate_initial_parameters())

    extrapolated = model(np.arange(train_size, size), *popt)

    return (
        [train_size + trade for trade in get_optimal_trades(extrapolated)],
        lambda x: model(x, *popt),
        popt,
    )

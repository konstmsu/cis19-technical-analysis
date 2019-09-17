from typing import List

import numpy as np
from scipy.optimize import curve_fit, differential_evolution

from app.trade_optimizer import get_optimal_trades


def solve(train_price: np.ndarray, test_size: int) -> List[int]:
    train_size = train_price.shape[0]
    train_x = np.arange(train_size)

    # pylint: disable=invalid-name,too-many-arguments
    def model(
        x,
        base,
        trend,
        scale0,
        period0,
        scale1,
        period1,
        scale2,
        period2,
        scale3,
        period3,
    ):
        result = base + trend * x / (train_size + test_size)
        for scale, period in (
            (scale0, period0),
            (scale1, period1),
            (scale2, period2),
            (scale3, period3),
        ):
            result += scale * np.sin(x * 2 * np.pi / period)
        return result

    def generate_initial_parameters():
        def model_error(model_parameters):
            return np.sum((train_price - model(train_x, *model_parameters)) ** 2.0)

        parameter_bounds = []
        parameter_bounds.append([200, 300])
        parameter_bounds.append([-100, 100])
        argcount = model.__code__.co_argcount - 3
        for _ in range(0, argcount, 2):
            parameter_bounds.append([5, 15])
            parameter_bounds.append([10, 100])

        result = differential_evolution(model_error, parameter_bounds)
        return result.x

    popt, _ = curve_fit(model, train_x, train_price, p0=generate_initial_parameters())

    extrapolated = model(np.arange(train_size, train_size + test_size), *popt)

    return [train_size + trade for trade in get_optimal_trades(extrapolated)]

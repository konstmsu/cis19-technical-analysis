from typing import List

import numpy as np
from scipy.optimize import curve_fit

from app.trade_optimizer import get_optimal_trades


def fit_all_models(train_price: np.ndarray) -> List[tuple]:
    train_size = train_price.shape[0]

    models = [
        # pylint: disable=unnecessary-lambda
        lambda x, base: np.full_like(x, base),
        lambda x, base, trend: base + trend / (train_size - 1) * x,
        lambda x, base, trend, scale0, width0: base
        + trend / (train_size - 1) * x
        + scale0 * np.sin(x * width0),
        lambda x, base, trend, scale0, width0, scale1, width1: base
        + trend / (train_size - 1) * x
        + scale0 * np.sin(x * width0)
        + scale1 * np.sin(x * width1),
        lambda x, base, trend, scale0, width0, scale1, width1, scale2, width2: base
        + trend / (train_size - 1) * x
        + scale0 * np.sin(x * width0)
        + scale1 * np.sin(x * width1)
        + scale2 * np.sin(x * width2),
    ]

    return [
        (
            model,
            *curve_fit(
                model,
                np.arange(train_size),
                train_price,
                p0=[200, 20, 5, 20, 6, 50, 7, 110][: model.__code__.co_argcount - 1],
                absolute_sigma=True,
                maxfev=10000,
            ),
        )
        for model in models
    ]


def solve(train_price: np.ndarray, test_size: int) -> List[tuple]:
    fits = fit_all_models(train_price)
    train_size = train_price.shape[0]
    model, popt, _ = fits[1]

    extrapolated = model(np.arange(train_size, train_size + test_size), *popt)

    return [train_size + trade for trade in get_optimal_trades(extrapolated)]

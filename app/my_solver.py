from typing import List

import numpy as np
from scipy.optimize import curve_fit

from app.trade_optimizer import get_optimal_trades


def fit_all_models(train_price: np.ndarray) -> List[tuple]:
    train_size = train_price.shape[0]

    models = [
        lambda x, base: np.full_like(train_price, base),
        lambda x, base, trend: base + trend / (train_size - 1) * x,
        lambda x, base, trend, scale0, width0: base
        + trend / (train_size - 1) * x
        + scale0 * np.sin(x * width0),
    ]

    return [
        (model, *curve_fit(model, np.arange(train_size), train_price))
        for model in models
    ]


def solve(train_price: np.ndarray, test_size: int) -> List[tuple]:
    fits = fit_all_models(train_price)
    train_size = train_price.shape[0]
    model, popt, pcov = fits[1]

    extrapolated = model(np.arange(train_size, train_size + test_size), *popt)

    return [train_size + trade for trade in get_optimal_trades(extrapolated)]

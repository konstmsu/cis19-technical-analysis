#%%
import importlib
import pprint

import matplotlib.pyplot as plt
import numpy as np

from app import generation, evaluate, trade_simulator, trade_optimizer

importlib.reload(generation)
importlib.reload(evaluate)
importlib.reload(trade_simulator)


def simulate(name, scenario, trades):
    fig = plt.figure()
    fig.set_size_inches(9, 4)
    plt.plot(scenario.get_train_price(), "g")
    plt.plot(
        np.arange(scenario.test_size) + scenario.train_size, scenario.test_signal, "y"
    )
    plt.vlines(
        trades[::2], scenario.test_signal.min(), scenario.test_signal.max(), "y", "--"
    )
    plt.vlines(
        trades[1::2], scenario.test_signal.min(), scenario.test_signal.max(), "m", "--"
    )
    plt.savefig(f"art/{name}.png")
    amount = trade_simulator.simulate(scenario.test_signal, scenario.train_size, trades)
    print(f"Optimal trades: {trades}")
    print(f"The optimal amount is {amount:.2f}")
    print()


def display_scenarios(names, scenarios):
    solutions = []
    for name, scenario in zip(names, scenarios):
        optimal_trades = list(trade_optimizer.get_optimal_trades(scenario.test_signal))
        simulate(
            name, scenario, [trade + scenario.train_size for trade in optimal_trades]
        )
        print(name, " + ".join(scenario.signal_description))
        solutions.append(optimal_trades)

    challenge_input = evaluate.create_challenge_input(scenarios)
    print(pprint.pprint(challenge_input, width=120, compact=True))
    print("Solutions:")
    print(pprint.pprint(solutions))


display_scenarios(
    ["one", "two"],
    [
        generation.ScenarioBuilder(0, 20, 40).add_base()
        # .add_trend()
        .add_waves(2, period_count_range=(2, 2)).add_noise(),
        generation.ScenarioBuilder(0, 20, 40).add_base()
        # .add_trend()
        .add_waves(4, period_count_range=(2, 4)).add_noise(),
    ],
)

#%%
from app import my_solver

importlib.reload(generation)
importlib.reload(my_solver)


def run_all_fits():
    scenario = (
        generation.ScenarioBuilder(0, 200, 400).add_base()
        # .add_trend()
        .add_waves(1, period_count_range=(2, 4))
        # .add_noise()
    )

    fits = my_solver.fit_all_models(scenario.get_train_price())

    plt.plot(scenario.signal)
    plt.axvline(scenario.train_size, linestyle="--")
    for model, popt, pcov in fits:
        plt.plot(model(np.arange(scenario.size), *popt))
        pprint.pprint(popt)


run_all_fits()

#%%
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pprint
from scipy.optimize import differential_evolution


def test_curve_fit():
    x = np.arange(100)
    y = 10 * np.sin(x * 2 * np.pi / 50)
    plt.plot(y)

    def model(xx, scale, period):
        return scale * np.sin(xx * 2 * np.pi / period)

    # function for genetic algorithm to minimize (sum of squared error)
    def sumOfSquaredError(parameterTuple):
        val = model(x, *parameterTuple)
        return np.sum((y - val) ** 2.0)

    def generate_Initial_Parameters():
        # min and max used for bounds
        maxX = max(x)
        minX = min(x)
        maxY = max(y)
        minY = min(y)
        maxXY = max(maxX, maxY)

        parameterBounds = []
        parameterBounds.append([-maxXY, maxXY]) # seach bounds for c
        parameterBounds.append([-maxXY, maxXY]) # seach bounds for c

        # "seed" the numpy random number generator for repeatable results
        result = differential_evolution(sumOfSquaredError, parameterBounds, seed=3)
        return result.x

    # generate initial parameter values
    geneticParameters = generate_Initial_Parameters()

    topt, tcov = curve_fit(model, x, y, p0=geneticParameters, absolute_sigma=True)
    pprint.pprint(topt)
    y_pred = model(x, *topt)
    plt.plot(y_pred)


test_curve_fit()

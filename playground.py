#%%
import importlib
import pprint

import matplotlib.pyplot as plt
import numpy as np

from app import generation, evaluate, trade_simulator, trade_optimizer, my_solver

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
        trades = my_solver.solve(scenario.get_train_price(), scenario.test_size)
        optimal_trades = list(trade_optimizer.get_optimal_trades(scenario.test_signal))
        simulate(name, scenario, trades)
        print(name, " + ".join(scenario.signal_description))
        solutions.append(optimal_trades)

    challenge_input = evaluate.create_challenge_input(scenarios)
    print(pprint.pprint(challenge_input, width=120, compact=True))
    print("Solutions:")
    print(pprint.pprint(solutions))


display_scenarios(
    ["one", "two", "three", "four"],
    generation.get_standard_scenarios(0),
)

#%%
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pprint
from scipy.optimize import differential_evolution
from app.generation import ScenarioBuilder


def test_curve_fit():
    x = np.arange(100)
    scenario = (
        ScenarioBuilder(2, 100, 1000).add_base().add_trend().add_waves(4).add_noise()
    )
    y = scenario.get_train_price()
    plt.plot(y)

    def model(
        xx,
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
        result = base + trend * xx / x.shape[0]
        for scale, period in (
            (scale0, period0),
            (scale1, period1),
            (scale2, period2),
            (scale3, period3),
        ):
            result += scale * np.sin(xx * 2 * np.pi / period)
        return result

    # function for genetic algorithm to minimize (sum of squared error)
    def sumOfSquaredError(parameterTuple):
        return np.sum((y - model(x, *parameterTuple)) ** 2.0)

    def generate_initial_parameter():
        parameter_bounds = []
        parameter_bounds.append([200, 300])
        parameter_bounds.append([-100, 100])
        argcount = model.__code__.co_argcount - 3
        for _ in range(0, argcount, 2):
            parameter_bounds.append([5, 15])
            parameter_bounds.append([20, 40])

        result = differential_evolution(
            sumOfSquaredError, parameter_bounds, seed=3, maxiter=100
        )
        return result.x

    initial_parameters = generate_initial_parameter()

    topt, tcov = curve_fit(model, x, y, p0=initial_parameters, absolute_sigma=True)
    pprint.pprint(topt)
    y_pred = model(x, *topt)
    plt.plot(y_pred)


test_curve_fit()

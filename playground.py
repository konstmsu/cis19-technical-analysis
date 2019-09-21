#%%
import importlib
import pprint
import time

import matplotlib.pyplot as plt
import numpy as np

from app import generation, evaluate, trade_simulator, trade_optimizer, my_solver

importlib.reload(generation)
importlib.reload(evaluate)
importlib.reload(trade_simulator)
importlib.reload(my_solver)


def simulate(name, scenario: generation.Scenario):
    start = time.process_time()
    trades, model, popt = my_solver.solve(
        0, scenario.train_signal, scenario.test_size, scenario.sine_count
    )
    end = time.process_time()
    print(f"Took {end - start:.2f}s. Parameters: {scenario.model_parameters}")

    amount = trade_simulator.simulate(scenario.test_signal, scenario.train_size, trades)
    optimal_trades = list(trade_optimizer.get_optimal_trades(scenario.test_signal))
    optimal_amount = trade_simulator.simulate(scenario.test_signal, 0, optimal_trades)
    fig = plt.figure()
    fig.set_size_inches(16, 4)
    plt.plot(scenario.train_signal, "g")
    x_train = np.arange(scenario.train_size)
    x_test = np.arange(scenario.test_size) + scenario.train_size
    plt.plot(x_test, scenario.test_signal, "y")
    plt.savefig(f"art/{name}.png")

    test_model = model(x_test)
    plt.plot(x_test, test_model, "b")

    # line_min = scenario.test_signal.min()
    # line_max = scenario.test_signal.max()
    # plt.vlines(trades[::2], line_min, line_max, "y", "--")
    # plt.vlines(trades[1::2], line_min, line_max, "m", "--")

    if amount / optimal_amount < 0.99:
        plt.plot(x_train, scenario.train_signal - model(x_train), "m")
        plt.plot(x_test, scenario.test_signal - test_model, "m")
        print(f"Amount is {amount:.2f}, max_amount is {optimal_amount:.2f}")
        print(f"Model options: {popt}")
        # print(f"Trades: {trades}")
        # print(f"Optimal trades: {optimal_trades}")
        print()


def display_scenarios(scenarios):
    challenge_input = evaluate.create_challenge_input(scenarios)
    pprint.PrettyPrinter(width=120, compact=True).pprint(challenge_input)

    for i, scenario in enumerate(scenarios):
        name = str(i + 1)
        print(name)
        simulate(name, scenario)


display_scenarios(generation.get_standard_scenarios(1))

#%%
import importlib
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pprint
from scipy.optimize import differential_evolution
from app import generation, trade_simulator, trade_optimizer

importlib.reload(generation)


def test_curve_fit():
    scenario = (
        generation.ScenarioBuilder(2, 100, 1000)
        .set_base()
        .set_trend()
        .add_waves(4)
        .build()
    )
    y_train = (
        scenario.train_signal
    )  # + 5 * np.random.standard_normal(scenario.train_size)
    x_train = np.arange(scenario.train_size)
    plt.plot(y_train)

    x_scale = 1 / (scenario.size - 1)
    # pylint: disable=too-many-arguments,invalid-name
    def model(x, base, trend, *waves):
        """
        x: [0, n)
        waves: scale_i, period_i        
        """
        result = base + trend * x_scale * x

        for scale, period_count in zip(waves[::2], waves[1::2]):
            result += scale * np.sin(2 * np.pi * period_count * x_scale * x)

        return result

    def error(model_parameters):
        return np.sum((y_train - model(x_train, *model_parameters)) ** 2.0)

    def generate_initial_parameter():
        parameter_bounds = []
        parameter_bounds.append([200, 300])
        parameter_bounds.append([-100, 100])
        max_wave_count = 4
        for _ in range(max_wave_count):
            parameter_bounds.append([0, 20])
            parameter_bounds.append([20, 40])

        result = differential_evolution(error, parameter_bounds)
        return result.x

    initial_parameters = generate_initial_parameter()

    popt, pcov = curve_fit(model, x_train, y_train, p0=initial_parameters)
    print("Expected:", scenario.model_parameters)
    print("Actual:", popt)
    x_test = np.arange(scenario.train_size, scenario.size)
    y_pred = model(x_test, *popt)
    plt.plot(x_test, y_pred)
    plt.plot(x_test, scenario.test_signal)
    plt.plot(x_test, y_pred - scenario.test_signal)

    optimal_trades = list(trade_optimizer.get_optimal_trades(scenario.test_signal))
    print("Optimal trades:", optimal_trades)

    max_amount = trade_simulator.simulate(scenario.test_signal, 0, optimal_trades)

    amount = trade_simulator.simulate(
        scenario.test_signal, 0, list(trade_optimizer.get_optimal_trades(y_pred))
    )

    print(f"Amount max: {max_amount:.2f}, actual: {amount:.2f}")


test_curve_fit()

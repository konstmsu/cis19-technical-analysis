#%%
import importlib
import json
import pprint
import numpy as np
import matplotlib.pyplot as plt
from app import generation, trade_optimizer, trade_simulator, evaluate
from app import my_solver

importlib.reload(generation)
importlib.reload(evaluate)


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
fits = my_solver.fit_all_models(np.array([10, 12, 15, 14, 12, 11, 13, 16]))

for model, popt, pcov in fits:
    plt.plot(model(np.arange(20), *popt))

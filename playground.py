#%%
import importlib
import numpy as np
import matplotlib.pyplot as plt
from app import generation, trade_optimizer, trade_simulator

importlib.reload(generation)


def simulate(scenario, trades):
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
    amount = trade_simulator.simulate(scenario.test_signal, trades - scenario.train_size)
    print(f"Optimal trades: {trades}")
    print(f"The optimal amount is {amount:.2f}")
    print()


def draw_sample(s):
    trades = list(trade_optimizer.get_optimal_trades(s.test_signal))
    simulate(s, s.train_size + np.array(trades))
    print(" + ".join(s.signal_description))


draw_sample(generation.ScenarioBuilder(0, 100, 200)
    .add_base()
    .add_trend()
    .add_waves(2, period_count_range=(3, 5))
    .add_noise())

draw_sample(generation.ScenarioBuilder(0, 100, 200)
    .add_base()
    .add_trend()
    .add_waves(4, period_count_range=(8, 14))
    .add_noise())

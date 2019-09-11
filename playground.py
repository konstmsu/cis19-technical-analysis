#%%
import importlib
import numpy as np
import matplotlib.pyplot as plt
from app import generation, trade_optimizer, trade_simulator

importlib.reload(generation)


def simulate(signal, trades):
    plt.figure()
    plt.plot(signal, "g")
    # plt.gca().set_ylim(0)
    plt.vlines(trades[::2], signal.min(), signal.max(), "y", "--")
    plt.vlines(trades[1::2], signal.min(), signal.max(), "m", "--")
    amount = trade_simulator.simulate(signal, trades)
    print(f"The optimal amount is {amount:.2f}")


for scenario in generation.get_standard_scenarios(0):
    tt = list(trade_optimizer.get_optimal_trades(scenario.test_signal))
    simulate(scenario.signal, scenario.train_size + np.array(tt))

#%%
import numpy as np
import matplotlib.pyplot as plt
import json
import glob
import os.path
import itertools
from snapshottest import snapshot
import importlib
from app import generation, trade_optimizer, trade_simulator


def plot(y):
    plt.plot(y, "r+", y)
    plt.figure()


def simulate(price, trades):
    trades = list(trades)
    signal = price[0]
    plt.plot(signal, "g")
    plt.vlines(trades[::2], signal.min(), signal.max(), "y", "--")
    plt.vlines(trades[1::2], signal.min(), signal.max(), "m", "--")
    amount = trade_simulator.simulate(signal, trades)
    print(f"The final amount is {amount:.2f}")


train_n = 50
test_n = 100
price_generator = generation.PriceGenerator(42)
price = price_generator.generate_price(train_n + test_n)

plot(np.sum(price, axis=0))
simulate(price, trade_optimizer.get_optimal_trades(price[0]))

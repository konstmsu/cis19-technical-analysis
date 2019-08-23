# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%%
import numpy as np
import matplotlib.pyplot as plt


#%%
def get_trend(n):
    return np.arange(n) / (n - 1)


def get_saw(n, period_length):
    return np.mod(np.arange(n), period_length) / (period_length - 1)


def get_wave(n, period_length):
    return 0.5 + 0.5 * np.sin(2 * np.pi / period_length * np.arange(n))


def get_waves(n, period_lengths):
    waves = [get_wave(n, l) for l in period_lengths]
    return np.sum(waves, axis=0)


def get_noise(n):
    return np.random.randn(n)


n = 201
y = get_waves(n, [100, 75]) + get_saw(n, 40) + 3 * get_trend(n) + 0.1 * get_noise(n)

plt.plot(y, "r+", y)


#%%
from collections import namedtuple
from scipy.signal import argrelextrema, find_peaks

n = 400
offset = 41
no = n + offset
signal = (get_waves(no, [100, 75]) + get_saw(no, 40) + 3 * get_trend(no))[offset:]
noise = 0.1 * get_noise(n)


def get_trades(price):
    mins = argrelextrema(price, np.less_equal)[0]
    maxs = argrelextrema(price, np.greater_equal)[0]

    if maxs[0] < mins[0]:
        maxs = maxs[1:]

    if maxs[-1] < mins[-1]:
        mins = mins[:-1]

    return np.union1d(mins, maxs)


def get_final_amount(price, trades):
    amount = 1
    #    if len(trades) % 2 == 1:
    #        trades = np.append(trades, trades[-1])

    for i in range(0, len(trades), 2):
        prev_amount = amount
        buy = price[trades[i]]
        sell = price[trades[i + 1]]
        count = amount / buy
        amount = count * sell
        print(f"Buy at {buy}, sell at {sell}, new amount is {amount}")
        assert prev_amount <= amount, f"Traded at loss at {i}-{i+1}"
    return amount


plt.plot(signal, "g")
trades = get_trades(signal)
plt.vlines(trades[::2], signal.min(), signal.max(), "y", "--")
plt.vlines(trades[1::2], signal.min(), signal.max(), "m", "--")
amount = get_final_amount(signal, trades)
print(f"Final amount is {amount}")


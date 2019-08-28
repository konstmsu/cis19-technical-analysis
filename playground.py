#%%
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
import operator
import json
import glob
import os.path
import itertools
from snapshottest import snapshot
import importlib


def get_trend(n):
    return np.arange(n) / (n - 1)


def get_saw(n, period_length):
    return np.mod(np.arange(n), period_length) / (period_length - 1)


def get_wave(n, period_length):
    return 0.5 + 0.5 * np.sin(2 * np.pi / period_length * np.arange(n))


def get_waves(n, period_lengths):
    components = (get_wave(n, l) for l in period_lengths)
    return reduce(operator.add, components, np.zeros(n))


def get_noise(n):
    return np.random.randn(n)


def generate_price(n):
    # TODO Add offset to avoid zero sines @ 0
    signal = np.ones(n)
    signal += 1 * get_waves(n, [n // 3])
    # signal += 1 * get_saw(n, n // 5)
    # signal += 1 * get_trend(n)
    noise = 0.0 * get_noise(n)
    return np.stack((signal, noise))


def plot(y):
    plt.plot(y, "r+", y)
    plt.figure()


def get_optimal_trades(price):
    mins = find_peaks(-price)[0]
    maxs = find_peaks(price)[0]

    print(f"Mins: {mins}")
    print(f"Maxs: {maxs}")

    if maxs[0] < mins[0]:
        maxs = maxs[1:]

    if maxs[-1] < mins[-1]:
        mins = mins[:-1]

    return np.union1d(mins, maxs)


def get_final_amount(price, trades):
    amount = 1

    for i in range(0, len(trades) - 1, 2):
        prev_amount = amount
        buy = price[trades[i]]
        sell = price[trades[i + 1]]
        count = amount / buy
        amount = count * sell
        print(f"Buy at {buy:.2f}, sell at {sell:.2f}, new amount is {amount:.2f}")
        # assert prev_amount <= amount, f"Traded at loss at {i}-{i+1}"

    return amount


def simulate(price, trades):
    signal = price[0]
    plt.plot(signal, "g")
    plt.vlines(trades[::2], signal.min(), signal.max(), "y", "--")
    plt.vlines(trades[1::2], signal.min(), signal.max(), "m", "--")
    amount = get_final_amount(signal, trades)
    print(f"The final amount is {amount:.2f}")


def analyze(sample, test_n):
    return []


def get_new_filename(filename_template):
    for i in itertools.count():
        filename = filename_template.format(i)
        if not os.path.isfile(filename):
            return filename


def write_test_data(description, data):
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    filename = get_new_filename(f"test/{description}_{{0:03d}}.json")
    with open(filename, "w") as f:
        json.dump(data, f, cls=NumpyEncoder)
    print(f"Written to {filename}")


def optimal_tests():
    price_inputs = glob.glob("test/price_*.json")
    assert len(price_inputs) > 0
    for i in price_inputs:
        with open(i) as f:
            data = np.asarray(json.load(f))
        result = get_optimal_trades(data[0])
        # snapshot.assert_match(result)


train_n = 50
test_n = 100
price = generate_price(train_n + test_n)

# write_test_data("price", price)
optimal_tests()

plot(np.sum(price, axis=0))
simulate(price, get_optimal_trades(price[0]))

#%%
values = np.asarray([1, 5, 6, 6, 3])
diff = np.diff(values)
ups = diff > 0
downs = diff < 0
moves = np.argwhere(ups | downs)
extrema = ups[moves[:-1]] & downs[moves[1:]]
moves[:-1][extrema]

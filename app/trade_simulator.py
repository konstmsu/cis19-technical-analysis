def simulate(signal, trades):
    trades = list(trades)

    if trades:
        earliest_trade = min(trades)
        if earliest_trade < 0:
            raise Exception(f"Trade {earliest_trade} is out of range")

        lastest_trade = max(trades)
        if lastest_trade >= len(signal):
            raise Exception(f"Trade {lastest_trade} is out of range")

    money = 1
    security = 0

    for trade in sorted(trades):
        price = signal[trade]
        if security:
            money = price * security
            security = 0
        else:
            security = money / price
            money = 0

    if security:
        money = signal[-1] * security

    return money


def get_score(optimal_result, result):
    return min(1, max(0, (result - 1) / (optimal_result - 1)))

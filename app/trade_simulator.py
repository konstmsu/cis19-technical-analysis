def simulate(signal, trades):
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

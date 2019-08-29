def simulate(prices, trades):
    money = 1
    security = 0

    for t in sorted(trades):
        price = prices[t]
        if security:
            money = price * security
            security = 0
        else:
            security = money / price
            money = 0

    if security:
        money = prices[-1] * security

    return money

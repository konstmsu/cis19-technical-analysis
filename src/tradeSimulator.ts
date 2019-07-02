export function simulate(prices: number[], trades: number[]) {
  const sortedTrades = [...trades].sort();

  let money = 1.0;
  let equity = 0;
  let holdingEquity = false;

  const buyEquity = (price: number) => {
    equity = money / price;
    money = 0;
    holdingEquity = true;
  };

  function sellEquity(price: number) {
    money = equity * price;
    equity = 0;
    holdingEquity = false;
  }

  for (const t of sortedTrades) {
    const price = prices[t];

    if (holdingEquity) {
      sellEquity(price);
    } else {
      buyEquity(price);
    }
  }

  if (holdingEquity) {
    sellEquity(prices[prices.length - 1]);
  }

  return money;
}

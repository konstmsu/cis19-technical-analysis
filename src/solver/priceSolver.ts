export function constantSolver(prices: number[], testSize: number) {
  return [];
}

export function linearSolver(prices: number[], testSize: number) {
  if (prices[0] >= prices[prices.length - 1]) {
    return [];
  }
  return [0, testSize - 1];
}

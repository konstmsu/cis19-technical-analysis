import { randomSeq } from "../priceGenerator";
import { simulate } from "../tradeSimulator";
import { constantSolver } from "./priceSolver";

function runProblem(
  generatePrices: (count: number) => number[],
  trainSize: number,
  testSize: number,
  solve: (prices: number[], testSize: number) => number[],
) {
  const prices = generatePrices(trainSize + testSize);
  const training = prices.slice(0, trainSize);
  const test = prices.slice(trainSize);
  const trades = solve(training, testSize);
  return simulate(test, trades);
}

describe("price solver", () => {
  it("solve constant", () => {
    const result = runProblem(randomSeq, 100, 1000, constantSolver);
    expect(result).toEqual(1.0);
  });
});

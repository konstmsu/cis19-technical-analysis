import { linearSeq, randomSeq } from "../priceGenerator";
import { simulate } from "../tradeSimulator";
import { constantSolver, linearSolver } from "./priceSolver";

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
    const result = runProblem(randomSeq, 10, 100, constantSolver);
    expect(result).toEqual(1.0);
  });

  it("solve linear increasing", () => {
    const result = runProblem(linearSeq(9, 12), 2, 5, linearSolver);
    expect(result).toBeCloseTo(1.2, 5);
  });
});

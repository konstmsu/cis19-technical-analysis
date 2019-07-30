import { linearSeq, randomSeq, sinSeq } from "../priceGenerator";
import { simulate } from "../tradeSimulator";
import { constantSolver, linearSolver, sinSolver } from "./priceSolver";
import { pi } from "mathjs";

function runProblem(
  generatePrices: (count: number) => number[],
  trainSize: number,
  testSize: number,
  solve: (prices: number[], testSize: number) => number[]
) {
  const prices = generatePrices(trainSize + testSize);
  const trainingSet = prices.slice(0, trainSize);
  const testSet = prices.slice(trainSize);
  const trades = solve(trainingSet, testSize);
  return { trainingSet, testSet, trades, amount: simulate(testSet, trades) };
}

describe("price solver", () => {
  it("solve constant", () => {
    const result = runProblem(randomSeq, 10, 100, constantSolver);
    expect(result.amount).toEqual(1.0);
  });

  it("solve linear increasing", () => {
    const result = runProblem(linearSeq(9, 12), 2, 5, linearSolver);
    expect(result.amount).toBeCloseTo(1.2, 5);
  });

  it("solve linear decresing", () => {
    const result = runProblem(linearSeq(12, 7), 2, 4, linearSolver);
    expect(result.amount).toBeCloseTo(1, 5);
  });

  it("sin price seq", () => {
    expect(
      sinSeq(0, 2 * pi * 1.5)(19).map(v => v.toFixed(4))
    ).toMatchSnapshot();
  });

  it("solve sin", () => {
    const sinPriceSeq = (count: number) =>
      sinSeq(0, 2 * pi * 3)(count).map(v => v * 0.5 + 1.5);

    const result = runProblem(sinPriceSeq, 12, 25, sinSolver);
    expect(result.trainingSet.map(v => v.toFixed(4))).toMatchSnapshot(
      "trainingSet"
    );
    expect(result.testSet.map(v => v.toFixed(4))).toMatchSnapshot("testSet");
    expect(result.amount).toBeCloseTo(3, 5);
  });
});

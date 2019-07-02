import { simulate } from "./tradeSimulator";

describe("trade simulator", () => {
  it("no changes when no trades", () => {
    expect(simulate([10, 15], [])).toEqual(1.0);
  });

  it("buy low sell high", () => {
    expect(simulate([10, 20], [0, 1])).toEqual(2.0);
  });

  it("buy high sell low", () => {
    expect(simulate([15, 10, 9], [1, 2])).toEqual(0.9);
  });

  it("last trade was buy", () => {
    expect(simulate([10, 15, 4], [0, 1, 2])).toEqual(1.5);
  });

  it("always sell at the end", () => {
    expect(simulate([10, 15], [0])).toEqual(1.5);
  });

  it("sort trades", () => {
    expect(simulate([20, 10], [1, 0])).toEqual(0.5);
  });
});

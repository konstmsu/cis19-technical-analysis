import { getLocalExtrema } from "./localExtrema";
import { randomInt } from "mathjs";

describe("local extrema", () => {
  it("empty", () => {
    expect(getLocalExtrema([])).toEqual({
      firstExtremumKind: "EmptyInput",
      indexes: []
    });
  });

  it("single value", () => {
    expect(getLocalExtrema([42])).toEqual({
      firstExtremumKind: "Constant",
      indexes: [0]
    });
  });

  it("increasing", () => {
    expect(getLocalExtrema([11, 12])).toEqual({
      firstExtremumKind: "Minimum",
      indexes: [0, 1]
    });
  });

  it("increasing longer", () => {
    expect(getLocalExtrema([11, 12, 17])).toEqual({
      firstExtremumKind: "Minimum",
      indexes: [0, 2]
    });
  });

  it("decreasing", () => {
    expect(getLocalExtrema([115, 42])).toEqual({
      firstExtremumKind: "Maximum",
      indexes: [0, 1]
    });
  });

  it("decreasing longer", () => {
    expect(getLocalExtrema([115, 42, -14, -18])).toEqual({
      firstExtremumKind: "Maximum",
      indexes: [0, 3]
    });
  });

  it("not changing", () => {
    expect(getLocalExtrema([2, 2])).toEqual({
      firstExtremumKind: "Constant",
      indexes: []
    });
  });

  it("not changing extrema", () => {
    expect(getLocalExtrema([9, 7, 7, 8])).toEqual({
      firstExtremumKind: "Maximum",
      indexes: [0, 1, 3]
    });
  });

  it("constant tail", () => {
    expect(getLocalExtrema([5, 6, 6, 6])).toEqual({
      firstExtremumKind: "Minimum",
      indexes: [0, 3]
    });
  });

  it("contant head and tail", () => {
    expect(getLocalExtrema([8, 8, 8, 6, 6])).toEqual({
      firstExtremumKind: "Maximum",
      indexes: [0, 4]
    });
  });

  it("contant head", () => {
    expect(getLocalExtrema([6, 6, 8, 8, 9])).toEqual({
      firstExtremumKind: "Minimum",
      indexes: [0, 4]
    });
  });

  it("falling, stable, falling, stable, falling", () => {
    expect(getLocalExtrema([9, 8, 8, 8, 7, 7, 6])).toEqual({
      firstExtremumKind: "Maximum",
      indexes: [0, 6]
    });
  });

  it("random stress", () => {
    const runRandomTest = () => {
      const numbers = randomInt([1000], -3, 4) as number[];
      const extrema = getLocalExtrema(numbers);
      expect(extrema.indexes[0]).toEqual(0);
      let isMovingFromMax = extrema.firstExtremumKind === "Maximum";
      let extremumIndex = 1;
      for (let i = 1; i < numbers.length; i++) {
        const d = numbers[i] - numbers[i - 1];
        if (isMovingFromMax) expect(d).toBeLessThanOrEqual(0);
        else expect(d).toBeGreaterThanOrEqual(0);
        if (extrema.indexes[extremumIndex] == i) {
          extremumIndex++;
          isMovingFromMax = !isMovingFromMax;
        }
      }
      expect(extremumIndex).toEqual(extrema.indexes.length);
    };

    for (let i = 0; i < 100; i++) {
      runRandomTest();
    }
  });
});

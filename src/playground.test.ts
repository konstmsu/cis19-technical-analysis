import { randomInt, min, max } from "mathjs";
import { range } from "./math";

describe("playground", () => {
  it("randomInt", () => {
    const numbers = randomInt([100], -2, 2.1) as number[];
    expect(new Set(numbers)).toEqual(new Set([-2, -1, 0, 1, 2]));
  });
});

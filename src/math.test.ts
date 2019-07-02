import { linspace } from "./math";

describe("linspace", () => {
  it("two points", () => {
    expect(linspace(3, 4, 2)).toEqual([3, 4]);
  });

  it("one point", () => {
    expect(linspace(10, 15, 1)).toEqual([10]);
  });

  it("round numbers", () => {
    expect(linspace(10, 13, 4)).toEqual([10, 11, 12, 13]);
  });

  it("decreasing", () => {
    expect(linspace(1, -2, 4)).toEqual([1, 0, -1, -2]);
  });

  it("fractions", () => {
    expect(linspace(1.25, -0.25, 7)).toEqual([
      1.25,
      1.0,
      0.75,
      0.5,
      0.25,
      0,
      -0.25,
    ]);
  });
});

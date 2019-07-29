import { getInnerExtrema } from "./innerExtrema";

describe("inner extrema", () => {
  it("empty", () => expect(getInnerExtrema([])).toEqual([]));
  it("single", () => expect(getInnerExtrema([42])).toEqual([]));
  it("pair", () => expect(getInnerExtrema([1, 2])).toEqual([]));
  it("increasing", () => expect(getInnerExtrema([-10, -8, 5, 42])).toEqual([]));
  it("decreasing", () => expect(getInnerExtrema([100, 50, 3, 2])).toEqual([]));
  it("const2", () => expect(getInnerExtrema([30, 30])).toEqual([]));
  it("const3", () => expect(getInnerExtrema([30, 30, 30])).toEqual([]));
  it("const4", () => expect(getInnerExtrema([5, 5, 5, 5])).toEqual([]));

  it("const, up", () => expect(getInnerExtrema([6, 6, 7])).toEqual([]));
  it("const, down", () => expect(getInnerExtrema([7, 7, 4])).toEqual([]));
  it("down, const", () => expect(getInnerExtrema([9, 7, 7])).toEqual([]));
  it("up, const", () => expect(getInnerExtrema([2, 6, 6])).toEqual([]));

  it("up, down", () => expect(getInnerExtrema([4, 8, 6])).toEqual([1]));
  it("down, up", () => expect(getInnerExtrema([6, -7, -5])).toEqual([1]));
  it("down, down, up, up", () =>
    expect(getInnerExtrema([6, 3, -1, 2, 9])).toEqual([2]));
  it("up, up, down", () => expect(getInnerExtrema([2, 3, 6, 3])).toEqual([2]));
  it("const, up, up, const, const, down", () =>
    expect(getInnerExtrema([2, 2, 4, 5, 5, 5, 3])).toEqual([3]));
  it("const, up, up, const, const, up", () =>
    expect(getInnerExtrema([2, 2, 4, 5, 5, 5, 6])).toEqual([]));
  it("up, down, const, up, up, const", () =>
    expect(getInnerExtrema([4, 6, 5, 5, 7, 9, 9])).toEqual([1, 2]));
  it("const, up, const, down, const, const, down, const, const, up", () =>
    expect(getInnerExtrema([5, 5, 7, 7, 6, 6, 6, 5, 5, 5, 7])).toEqual([2, 7]));
  it("down, up, up, down, const, up, up", () =>
    expect(getInnerExtrema([3, 1, 2, 4, 3, 3, 6, 8])).toEqual([1, 3, 4]));
});

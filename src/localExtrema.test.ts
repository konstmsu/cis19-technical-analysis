import { ExtremumKind, getLocalExtrema } from "./localExtrema";

describe("local extrema", () => {
  it("empty", () => {
    expect(getLocalExtrema([])).toEqual({
      firstExtremumKind: ExtremumKind.EmptyInput,
      indexes: [],
    });
  });

  it("single value", () => {
    expect(getLocalExtrema([42])).toEqual({
      firstExtremumKind: ExtremumKind.SingleValue,
      indexes: [0],
    });
  });

  it("increasing", () => {
    expect(getLocalExtrema([11, 12])).toEqual({
      firstExtremumKind: ExtremumKind.Minimum,
      indexes: [0, 1],
    });
  });

  it("increasing longer", () => {
    expect(getLocalExtrema([11, 12, 17])).toEqual({
      firstExtremumKind: ExtremumKind.Minimum,
      indexes: [0, 2],
    });
  });

  it("decreasing", () => {
    expect(getLocalExtrema([115, 42])).toEqual({
      firstExtremumKind: ExtremumKind.Maximum,
      indexes: [0, 1],
    });
  });

  it("decreasing longer", () => {
    expect(getLocalExtrema([115, 42, -14, -18])).toEqual({
      firstExtremumKind: ExtremumKind.Maximum,
      indexes: [0, 3],
    });
  });

  it("not changing", () => {
    expect(getLocalExtrema([2, 2])).toEqual({
      firstExtremumKind: ExtremumKind.Maximum,
      indexes: [0],
    });
  });

  it("not changing extrema", () => {
    expect(getLocalExtrema([9, 7, 7, 8])).toEqual({
      firstExtremumKind: ExtremumKind.Maximum,
      indexes: [0, 1, 3],
    });
  });

  it("constant tail", () => {
    expect(getLocalExtrema([5, 6, 6, 6])).toEqual({
      firstExtremumKind: ExtremumKind.Minimum,
      indexes: [0, 1],
    });
  });

  it("contant head and tail", () => {
    expect(getLocalExtrema([6, 6, 8, 8, 8])).toEqual({
      firstExtremumKind: ExtremumKind.Minimum,
      indexes: [0, 2],
    });
  });

  it("contant head", () => {
    expect(getLocalExtrema([6, 6, 8, 8, 9])).toEqual({
      firstExtremumKind: ExtremumKind.Minimum,
      indexes: [0, 4],
    });
  });

  it("falling, stable, falling, stable, falling", () => {
    expect(getLocalExtrema([9, 8, 8, 8, 7, 7, 6])).toEqual({
      firstExtremumKind: ExtremumKind.Maximum,
      indexes: [0, 6],
    });
  });
});

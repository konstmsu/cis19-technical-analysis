import { max, min, std, pi, sqrt } from "mathjs";
import { randomSeq, sinSeq } from "./priceGenerator";

describe("price generator", () => {
  it("generate random numbers", () => {
    const seq = randomSeq(100);

    expect(seq).toHaveLength(100);
    expect(0).toBeWithin(min(...seq), max(...seq));
    expect(std(seq)).toBeGreaterThan(0.5);
  });

  it("generate sin wave", () => {
    const seq = sinSeq(0, pi)(13);
    const rounded = (values: number[]) => values.map(v => v.toFixed(5));
    expect(rounded(seq)).toEqual(
      rounded([
        0,
        0.25882,
        1 / 2,
        1 / sqrt(2),
        sqrt(3) / 2,
        0.96593,
        1,
        0.96593,
        sqrt(3) / 2,
        1 / sqrt(2),
        1 / 2,
        0.25882,
        0
      ])
    );
  });

  it("generate longer sin wave", () => {
    const seq = sinSeq(0, pi * 4)(25);
    const rounded = (values: number[]) => values.map(v => v.toFixed(5));
    expect(rounded(seq)).toMatchSnapshot();
  });
});

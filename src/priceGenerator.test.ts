import { max, min, std } from "mathjs";
import { randomSeq } from "./priceGenerator";

describe("price generator", () => {
  it("generate random numbers", () => {
    const seq = randomSeq(100);

    expect(seq).toHaveLength(100);
    expect(0).toBeWithin(min(...seq), max(...seq));
    expect(std(seq)).toBeGreaterThan(0.5);
  });
});

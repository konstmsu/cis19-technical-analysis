import { add } from "./calculator";

describe("calculator", () => {
  it("add", () => {
    expect(add(1, 2)).toEqual(3);
  });
});

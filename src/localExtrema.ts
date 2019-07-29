import { abs, sign } from "mathjs";
import { range } from "./math";
import { getInnerExtrema, EPSILON } from "./innerExtrema";

export type ExtremumKind = "EmptyInput" | "Constant" | "Minimum" | "Maximum";

export interface ILocalExtrema {
  readonly firstExtremumKind: ExtremumKind;
  readonly indexes: number[];
}

export function getLocalExtrema(seq: number[]): ILocalExtrema {
  if (seq.length === 0) return { firstExtremumKind: "EmptyInput", indexes: [] };
  if (seq.length === 1) return { firstExtremumKind: "Constant", indexes: [0] };

  const innerExtrema = getInnerExtrema(seq);
  if (innerExtrema.length === 0) {
    const climb = seq[seq.length - 1] - seq[0];
    if (abs(climb) > EPSILON) {
      return {
        firstExtremumKind: climb < 0 ? "Maximum" : "Minimum",
        indexes: [0, seq.length - 1]
      };
    }

    return {
      firstExtremumKind: "Constant",
      indexes: []
    };
  }

  const result = [0, ...innerExtrema];

  const lastExtremum = innerExtrema[innerExtrema.length - 1];
  if (
    lastExtremum < seq.length &&
    abs(seq[lastExtremum] - seq[seq.length - 1]) > EPSILON
  )
    result.push(seq.length - 1);

  return {
    firstExtremumKind: seq[result[0]] > seq[result[1]] ? "Maximum" : "Minimum",
    indexes: result
  };
}

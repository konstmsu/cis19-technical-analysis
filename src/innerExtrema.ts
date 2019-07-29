import { range } from "./math";
import { abs } from "mathjs";

export const EPSILON = 1e-5;

export function getInnerExtrema(seq: number[]): number[] {
  if (seq.length < 3) return [];

  const diffs = range(0, seq.length - 1).map(i => seq[i + 1] - seq[i]);
  const moves = range(0, seq.length - 1).filter(i => abs(diffs[i]) > EPSILON);
  if (moves.length < 2) return [];

  const extrema_j = range(0, moves.length - 1).filter(j => {
    const d1 = diffs[moves[j]];
    const d2 = diffs[moves[j + 1]];
    return (d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0);
  });

  return extrema_j.map(j => moves[j] + 1);
}

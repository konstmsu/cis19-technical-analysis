import { linspace } from "./math";
import { sin } from "mathjs";

export function randomSeq(count: number) {
  const result = [];

  for (let i = 0; i < count; i++) {
    result.push(Math.random() * 2 - 1.0);
  }

  return result;
}

export function linearSeq(start: number, stop: number) {
  return (count: number) => linspace(start, stop, count);
}

export function sinSeq(start: number, stop: number) {
  return (count: number): number[] => {
    return linspace(start, stop, count).map(x => sin(x));
  };
}

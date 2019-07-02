export function linspace(start: number, stop: number, num: number): number[] {
  if (num === 1) {
    return [start];
  }
  if (num < 2) {
    return [];
  }

  const values = [];
  const n = num - 1;
  for (let i = 0; i <= n; i++) {
    const v = (i * stop + (n - i) * start) / n;
    values.push(v);
  }
  return values;
}

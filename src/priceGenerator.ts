export function randomSeq(count: number) {
  const result = [];

  for (let i = 0; i < count; i++) {
    result.push(Math.random() * 2 - 1.0);
  }

  return result;
}

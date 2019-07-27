export enum ExtremumKind {
  EmptyInput,
  SingleValue,
  Minimum,
  Maximum,
}

export interface ILocalExtrema {
  readonly firstExtremumKind: ExtremumKind;
  readonly indexes: number[];
}

export function getLocalExtrema(seq: number[]): ILocalExtrema {
  return { firstExtremumKind: ExtremumKind.SingleValue, indexes: [] };
}

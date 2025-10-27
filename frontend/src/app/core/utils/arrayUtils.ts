export function toSortedAsc<T>(array: T[], sortBy: (item: T) => number): T[] {
  return [...array].sort((a, b) => sortBy(a) - sortBy(b));
}

export function toSortedDesc<T>(array: T[], sortBy: (item: T) => number): T[] {
  return [...array].sort((a, b) => sortBy(b) - sortBy(a));
}

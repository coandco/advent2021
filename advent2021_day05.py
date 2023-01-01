from utils import read_data
from collections import Counter
from typing import NamedTuple, Set, Tuple, Generator


class Coord(NamedTuple):
    x: int
    y: int


def line_to_endpoints(line: str) -> Tuple[Coord, Coord]:
    first_str, second_str = line.split(" -> ")
    first_x, first_y = first_str.split(",")
    second_x, second_y = second_str.split(",")
    return Coord(x=int(first_x), y=int(first_y)), Coord(x=int(second_x), y=int(second_y))


def abs_range(num_one: int, num_two: int) -> Generator[int, None, None]:
    if num_two > num_one:
        yield from range(num_one, num_two+1)
    elif num_one > num_two:
        yield from range(num_one, num_two-1, -1)
    else:
        # If they're the same number, yield it indefinitely
        while True:
            yield num_one


def expand_endpoints(first: Coord, second: Coord, count_diagonals: bool = False) -> Set[Coord]:
    points = set()
    if count_diagonals or first.x == second.x or first.y == second.y:
        for x, y in zip(abs_range(first.x, second.x), abs_range(first.y, second.y)):
            points.add(Coord(x=x, y=y))
    return points


def main():
    INPUT = [line_to_endpoints(x) for x in read_data().splitlines()]
    counts = Counter()
    for endpoints in INPUT:
        counts.update(expand_endpoints(*endpoints))
    overlaps = len([x for x in counts if counts[x] > 1])
    print(f"Part one: {overlaps}")

    counts = Counter()
    for endpoints in INPUT:
        counts.update(expand_endpoints(*endpoints, count_diagonals=True))
    overlaps = len([x for x in counts if counts[x] > 1])
    print(f"Part two: {overlaps}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

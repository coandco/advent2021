from utils import read_data
from typing import NamedTuple, Tuple
from collections import deque
from math import prod
import numpy as np


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x+other.x, y=self.y+other.y)


NEIGHBORS = [
    Coord(x=-1, y=0),
    Coord(x=1, y=0),
    Coord(x=0, y=-1),
    Coord(x=0, y=1)
]


def in_bounds(shape: Tuple[int, int], coord: Coord):
    return (0 <= coord.y < shape[0]) and (0 <= coord.x < shape[1])


def is_local_minima(field: np.ndarray, loc: Coord) -> bool:
    if field[loc] == 9:
        return False
    for direction in NEIGHBORS:
        if in_bounds(field.shape, loc+direction) and field[loc+direction] <= field[loc]:
            return False
    return True


def get_basin_size(field: np.ndarray, loc: Coord) -> int:
    points_in_basin = {loc}
    points_to_check = deque([loc])
    while points_to_check:
        cur_loc = points_to_check.pop()
        for direction in NEIGHBORS:
            new_loc = cur_loc + direction
            if in_bounds(field.shape, new_loc) and new_loc not in points_in_basin and field[new_loc] != 9:
                points_in_basin.add(new_loc)
                points_to_check.append(new_loc)
    return len(points_in_basin)


def main():
    INPUT = [[int(x) for x in y] for y in read_data().splitlines()]
    INPUT_NP = np.array(INPUT, dtype=int)
    low_spots = set()
    for location, _ in np.ndenumerate(INPUT_NP):
        coord = Coord(*location)
        if is_local_minima(INPUT_NP, coord):
            low_spots.add(coord)
    low_spot_values = [INPUT_NP[x] for x in low_spots]
    print(f"Part one: {sum(low_spot_values) + len(low_spot_values)}")
    basin_sizes = sorted((get_basin_size(INPUT_NP, x) for x in low_spots), reverse=True)
    print(f"Part two: {prod(basin_sizes[:3])}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

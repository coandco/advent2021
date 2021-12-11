from utils import read_data
from typing import Tuple, NamedTuple
import numpy as np


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x+other.x, y=self.y+other.y)


NEIGHBORS = [
    Coord(-1, -1), Coord(-1, +0), Coord(-1, +1),
    Coord(+0, -1),                Coord(+0, +1),
    Coord(+1, -1), Coord(+1, +0), Coord(+1, +1)
]


def in_bounds(shape: Tuple[int, int], coord: Coord):
    return (0 <= coord.y < shape[0]) and (0 <= coord.x < shape[1])


def run_cycle(grid: np.ndarray) -> int:
    grid += 1
    flashed_coords = set()
    while coords_to_flash := [coord for x in zip(*np.where(grid > 9)) if (coord := Coord(*x)) not in flashed_coords]:
        for coord in coords_to_flash:
            for offset in NEIGHBORS:
                new_coord = coord + offset
                if in_bounds(grid.shape, new_coord):
                    grid[new_coord] += 1
            flashed_coords.add(coord)
    for coord in flashed_coords:
        grid[coord] = 0
    return len(flashed_coords)


if __name__ == '__main__':
    grid = np.genfromtxt(read_data().splitlines(), delimiter=1, dtype=int)
    total_flashes = 0
    cycles = 0
    while True:
        cycles += 1
        num_flashed = run_cycle(grid)
        if num_flashed == grid.shape[0] * grid.shape[1]:
            break
        total_flashes += num_flashed
        if cycles == 100:
            print(f"Part one: {total_flashes}")
    print(f"Part two: {cycles}")

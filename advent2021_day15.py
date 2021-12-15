from utils import read_data
from collections import deque
import numpy as np
import sys
from typing import NamedTuple, Tuple


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x+other.x, y=self.y+other.y)

NEIGHBORS = [
    Coord(-1, 0),
    Coord(1, 0),
    Coord(0, -1),
    Coord(0, 1)
]

PART_ONE_NEIGHBORS = [
    Coord(1, 0),
    Coord(0, 1)
]


def in_bounds(shape: Tuple[int, int], coord: Coord):
    return (0 <= coord.y < shape[0]) and (0 <= coord.x < shape[1])


def get_cost_to_goal(riskmap: np.ndarray) -> int:
    costs = np.full(riskmap.shape, fill_value=9999999, dtype=int)
    costs[0, 0] = 0
    open_nodes = {Coord(0, 0)}
    while open_nodes:
        current_loc, _ = min(((coord, costs[coord]) for coord in open_nodes), key=lambda x: x[1])
        if current_loc == Coord(riskmap.shape[0]-1, riskmap.shape[1]-1):
            return costs[-1, -1]
        open_nodes.remove(current_loc)
        for direction in NEIGHBORS:
            new_loc = current_loc + direction
            if in_bounds(riskmap.shape, new_loc):
                new_cost = costs[current_loc] + riskmap[new_loc]
                if new_cost < costs[new_loc]:
                    costs[new_loc] = new_cost
                    open_nodes.add(new_loc)
    return -1


def gen_part_two_grid(part_one_grid: np.ndarray) -> np.ndarray:
    part_two_grid = np.tile(part_one_grid, (5, 5))
    height, width = part_one_grid.shape
    for y in range(5):
        for x in range(5):
            part_two_grid[height*y:height*(y+1), width*x:width*(x+1)] += (x + y)
    part_two_grid[part_two_grid > 9] -= 9
    return part_two_grid


if __name__ == '__main__':
    INPUT = np.genfromtxt(read_data().splitlines(), delimiter=1, dtype=int)
    print(f"Part one: {get_cost_to_goal(INPUT)}")
    PART_TWO_INPUT = gen_part_two_grid(INPUT)
    print(f"Part two: {get_cost_to_goal(PART_TWO_INPUT)}")

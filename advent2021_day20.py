from utils import read_data
from typing import NamedTuple, Tuple, Set, List


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x+other.x, y=self.y+other.y)


NEIGHBORS = [
    Coord(-1, -1), Coord(-1, +0), Coord(-1, +1),
    Coord(+0, -1), Coord(+0, +0), Coord(+0, +1),
    Coord(+1, -1), Coord(+1, +0), Coord(+1, +1)
]


class Grid:
    index: List[bool]
    floormap: Set[Coord]
    cycle_num: int
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def __init__(self, data: str):
        index_str, grid_str = data.split("\n\n")
        self.index = [True if x == "#" else False for x in index_str]
        grid = set()
        for y, line in enumerate(grid_str.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    grid.add(Coord(x=x, y=y))
        self.grid = grid
        self.min_x, self.max_x = min(x.x for x in grid), max(x.x for x in grid)
        self.min_y, self.max_y = min(x.y for x in grid), max(x.y for x in grid)
        self.cycle_num = 1

    def output_grid(self):
        output = []
        for y in range(self.min_y, self.max_y + 1):
            line = "".join("#" if Coord(x=x, y=y) in self.grid else "." for x in range(self.min_x, self.max_x + 1))
            output.append(line)
        return "\n".join(output)

    def in_range(self, y, x):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def value_index(self, coord):
        # This used to use direct or/shift number manipulation, but it turns out string addition/intparse is faster(?!?)
        value = ""
        for neighbor in NEIGHBORS:
            # Doing manual non-Coord math here because this is the very innermost loop
            # and it's about twice as fast to just use raw Tuples instead of NamedTuples
            new_loc = (coord.y + neighbor.y, coord.x + neighbor.x)
            if self.cycle_num % 2 == 0:
                value += "1" if (not self.in_range(*new_loc)) or (new_loc in self.grid) else "0"
            else:
                value += "1" if new_loc in self.grid else "0"
        return int(value, 2)

    def new_value(self, coord):
        return self.index[self.value_index(coord)]

    def run_cycle(self) -> Set[Coord]:
        new_grid = set()
        for y in range(self.min_y - 4, self.max_y + 5):
            for x in range(self.min_x - 4, self.max_x + 5):
                pos = Coord(x=x, y=y)
                if self.new_value(pos):
                    new_grid.add(pos)
        if self.cycle_num % 2 == 0:
            self.min_x, self.max_x = min(x.x for x in self.grid), max(x.x for x in self.grid)
            self.min_y, self.max_y = min(x.y for x in self.grid), max(x.y for x in self.grid)
        else:
            self.min_x -= 3
            self.max_x += 3
            self.min_y -= 3
            self.max_y += 3
        self.grid = new_grid
        self.cycle_num += 1
        return new_grid


if __name__ == '__main__':
    floormap = Grid(read_data())
    for _ in range(2):
        floormap.run_cycle()
    print(f"Part one: {len(floormap.grid)}")
    for _ in range(48):
        floormap.run_cycle()
    print(f"Part two: {len(floormap.grid)}")

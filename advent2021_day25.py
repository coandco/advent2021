from utils import read_data
from typing import NamedTuple, Tuple, Set


DEBUG = False


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=(self.x+other.x) % SIZE_X, y=(self.y+other.y) % SIZE_Y)


def load_map(data: str) -> Tuple[Set[Coord], Set[Coord], int, int]:
    right = set()
    down = set()
    lines = data.splitlines()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '>':
                right.add(Coord(x=x, y=y))
            elif char == 'v':
                down.add(Coord(x=x, y=y))
    return right, down, len(lines[0]), len(lines)


def run_cycle(right: Set[Coord], down: Set[Coord]) -> Tuple[Set[Coord], Set[Coord], int]:
    new_right = set()
    new_down = set()
    movement = 0
    for coord in right:
        if (new_coord := coord+Coord(x=1, y=0)) in right or new_coord in down:
            new_right.add(coord)
        else:
            new_right.add(new_coord)
            movement += 1
    for coord in down:
        if (new_coord := coord+Coord(x=0, y=1)) in new_right or new_coord in down:
            new_down.add(coord)
        else:
            new_down.add(new_coord)
            movement += 1
    return new_right, new_down, movement


def print_field(rights: Set[Coord], downs: Set[Coord]):
    lines = []
    for y in range(SIZE_Y):
        line = ""
        for x in range(SIZE_X):
            coord = Coord(x=x, y=y)
            if coord in rights:
                line += ">"
            elif coord in downs:
                line += "v"
            else:
                line += "."
        lines.append(line)
    print("\n".join(lines) + "\n")


def main():
    global SIZE_X, SIZE_Y
    rights, downs, SIZE_X, SIZE_Y = load_map(read_data())
    if DEBUG:
        print_field(rights, downs)
    cycles = 0
    while True:
        rights, downs, movement = run_cycle(rights, downs)
        if DEBUG:
            print_field(rights, downs)
        cycles += 1
        if movement == 0:
            break
    print(f"Part one: {cycles}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

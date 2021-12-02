from utils import read_data
from typing import NamedTuple


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x + other.x, y=self.y + other.y)

    def __mul__(self, amount: int) -> 'Coord':
        return Coord(x=self.x * amount, y=self.y * amount)

    @staticmethod
    def from_str(line: str):
        direction, distance = line.split(" ", maxsplit=1)
        return PART_ONE_DIRECTIONS[direction] * int(distance)


class AimedCoord(NamedTuple):
    x: int
    y: int
    aim: int

    def __add__(self, other: 'AimedCoord') -> 'AimedCoord':
        return AimedCoord(x=self.x + other.x, y=self.y + (other.y * other.x * self.aim), aim=self.aim + other.aim)

    def __mul__(self, amount: int):
        return AimedCoord(x=self.x * amount, y=self.y, aim=self.aim*amount)

    @staticmethod
    def from_str(line: str):
        direction, distance = line.split(" ", maxsplit=1)
        return PART_TWO_DIRECTIONS[direction] * int(distance)


PART_ONE_DIRECTIONS = {
    'forward': Coord(x=1, y=0),
    'back': Coord(x=-1, y=0),
    'up': Coord(x=0, y=-1),
    'down': Coord(x=0, y=1)
}

PART_TWO_DIRECTIONS = {
    'forward': AimedCoord(x=1, y=1, aim=0),
    'up': AimedCoord(x=0, y=0, aim=-1),
    'down': AimedCoord(x=0, y=0, aim=1)
}

if __name__ == '__main__':
    PART_ONE_INPUT = [Coord.from_str(line) for line in read_data().splitlines()]
    part_one_position = sum(PART_ONE_INPUT, start=Coord(0, 0))
    print(f"Part one: {part_one_position.x * part_one_position.y}")

    PART_TWO_INPUT = [AimedCoord.from_str(line) for line in read_data().splitlines()]
    part_two_position = sum(PART_TWO_INPUT, start=AimedCoord(0, 0, 0))
    print(f"Part two: {part_two_position.x * part_two_position.y}")
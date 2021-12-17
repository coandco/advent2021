from utils import read_data
from typing import NamedTuple, Tuple, List


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x+other.x, y=self.y+other.y)


class TargetArea(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def hit(self, coord: Coord) -> bool:
        return self.min_x <= coord.x <= self.max_x and self.min_y <= coord.y <= self.max_y

    def overshot(self, coord: Coord, velocity: Coord) -> bool:
        return coord.x > self.max_x or (velocity.y < 0 and coord.y < self.min_y)

    @staticmethod
    def from_inputstr(data: str) -> 'TargetArea':
        x_str, y_str = data.split(", ", 1)
        min_x, max_x = [int(x) for x in x_str[len("target area: x="):].split("..")]
        min_y, max_y = [int(y) for y in y_str[len("y="):].split("..")]
        return TargetArea(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)


def simulate(velocity: Coord, target: TargetArea) -> bool:
    current_pos = Coord(0, 0)
    while not target.overshot(current_pos, velocity):
        current_pos = current_pos + velocity
        if target.hit(current_pos):
            return True
        dx = 0
        if velocity.x > 0:
            dx = -1
        elif velocity.x < 0:
            dx = 1
        velocity = velocity + Coord(x=dx, y=-1)
    return False


def part_one(target: TargetArea) -> int:
    vx = 1
    while (triangle_num := int(vx * (vx + 1) / 2)) <= target.max_x:
        if target.min_x <= triangle_num:
            break
        vx += 1
    vy = 1
    num_failures = 0
    last_success = 0
    while num_failures < 100:
        hit = simulate(Coord(x=vx, y=vy), target)
        if hit:
            last_success = vy
        num_failures = 0 if hit else num_failures + 1
        vy += 1
    return last_success


def part_two(target: TargetArea, max_vy: int) -> int:
    min_vx = 1
    while (triangle_num := min_vx*(min_vx+1)//2) <= target.max_x:
        if target.min_x <= triangle_num:
            break
        min_vx += 1
    num_successes = 0
    for vx in range(min_vx, target.max_x+1):
        for vy in range(target.min_y, max_vy+1):
            if simulate(Coord(x=vx, y=vy), target):
                num_successes += 1
    return num_successes


INPUT = TargetArea.from_inputstr(read_data())
max_vy = part_one(INPUT)
print(f"Part one: {max_vy * (max_vy + 1) // 2}")
print(f"Part two: {part_two(INPUT, max_vy)}")

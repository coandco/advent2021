from utils import read_data
from typing import NamedTuple


class TargetArea(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def hit(self, posx: int, posy: int) -> bool:
        return self.min_x <= posx <= self.max_x and self.min_y <= posy <= self.max_y

    def overshot(self, posx: int, posy: int, vy: int) -> bool:
        return posx > self.max_x or (vy < 0 and posy < self.min_y)

    @staticmethod
    def from_inputstr(data: str) -> 'TargetArea':
        x_str, y_str = data.split(", ", 1)
        min_x, max_x = [int(x) for x in x_str[len("target area: x="):].split("..")]
        min_y, max_y = [int(y) for y in y_str[len("y="):].split("..")]
        return TargetArea(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)


def simulate(vx: int, vy: int, target: TargetArea) -> bool:
    posx, posy = 0, 0
    while not target.overshot(posx, posy, vy):
        posx, posy = posx+vx, posy+vy
        if target.hit(posx, posy):
            return True
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
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
        hit = simulate(vx, vy, target)
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
            if simulate(vx, vy, target):
                num_successes += 1
    return num_successes


INPUT = TargetArea.from_inputstr(read_data())
max_vy = part_one(INPUT)
print(f"Part one: {max_vy * (max_vy + 1) // 2}")
print(f"Part two: {part_two(INPUT, max_vy)}")

from utils import read_data
from typing import NamedTuple, Iterator


class TargetArea(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def hit(self, posx: int, posy: int) -> bool:
        return posx in range(self.min_x, self.max_x+1) and posy in range(self.min_y, self.max_y+1)

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
        vx = vx-1 if vx > 0 else vx
        vy -= 1
    return False


def sim_x(vx: int) -> Iterator[int]:
    pos = 0
    while vx > 0:
        pos += vx
        yield pos
        vx -= 1


def part_two(target: TargetArea, max_vy: int) -> int:
    min_vx = 1
    while (triangle_num := min_vx*(min_vx+1)//2) <= target.max_x:
        if target.min_x <= triangle_num:
            break
        min_vx += 1
    return sum(simulate(vx, vy, target) for vx in range(min_vx, target.max_x+1) for vy in range(target.min_y, max_vy+1))


def main():
    target_area = TargetArea.from_inputstr(read_data())
    max_vy = abs(target_area.min_y) - 1
    print(f"Part one: {max_vy * (max_vy + 1) // 2}")
    print(f"Part two: {part_two(target_area, max_vy)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

from utils import read_data
from typing import NamedTuple, Tuple, List
import re

RE_NUMS = re.compile(r'[-]?\d+')


class Range(NamedTuple):
    x: range
    y: range
    z: range

    def overlap(self, other: 'Range') -> 'Range':
        return Range(range(max(self.x[0], other.x[0]), min(self.x[-1], other.x[-1])+1),
                     range(max(self.y[0], other.y[0]), min(self.y[-1], other.y[-1])+1),
                     range(max(self.z[0], other.z[0]), min(self.z[-1], other.z[-1])+1))

    def volume(self) -> int:
        return len(self.x)*len(self.y)*len(self.z)

    @staticmethod
    def from_str(line: str) -> 'Range':
        min_x, max_x, min_y, max_y, min_z, max_z = RE_NUMS.findall(line)
        return Range(x=range(int(min_x), int(max_x)+1),
                     y=range(int(min_y), int(max_y)+1),
                     z=range(int(min_z), int(max_z)+1))

    def __repr__(self):
        return f"Range(x={self.x[0]}..{self.x[-1]}, y={self.y[0]}..{self.y[-1]}, z={self.z[0]}..{self.z[1]})"


def total_nonintersecting_pixels(area: Range, possible_intersections: List[Range]):
    overlaps = [overlap for x in possible_intersections if (overlap := area.overlap(x)).volume() > 0]
    return area.volume() - sum(total_nonintersecting_pixels(x, overlaps[i+1:]) for i, x in enumerate(overlaps))


def part_one(data: List[Tuple[int, Range]]) -> int:
    start_area = Range(x=range(-50, 50 + 1), y=range(-50, 50 + 1), z=range(-50, 50 + 1))
    # Filter data down to just the bits that overlap with the start area
    data = [(op, overlap) for op, cube in data if (overlap := start_area.overlap(cube)).volume() > 0]
    pixels_on = 0
    for i, (op, cube) in enumerate(data):
        # We're using lookahead to only add pixels that will eventually be turned on.  Off commands turn zero pixels on.
        if op == "off":
            continue
        pixels_on += total_nonintersecting_pixels(cube, [x[1] for x in data[i+1:]])
    return pixels_on


def part_two(data: List[Tuple[int, Range]]) -> int:
    pixels_on = 0
    for i, (op, cube) in enumerate(data):
        # We're using lookahead to only add pixels that will eventually be turned on.  Off commands turn zero pixels on.
        if op == "off":
            continue
        pixels_on += total_nonintersecting_pixels(cube, [x[1] for x in data[i+1:]])
    return pixels_on


def main():
    ranges = [(x[:3].strip(), Range.from_str(x)) for x in read_data().splitlines()]

    print(f"Part one: {part_one(ranges)}")
    print(f"Part two: {part_two(ranges)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

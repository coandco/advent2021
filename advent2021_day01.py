from utils import read_data
from more_itertools import windowed
from typing import Iterable


def count_increases(data: Iterable) -> int:
    num_increases = 0
    for first, second in windowed(data, 2):
        if second > first:
            num_increases += 1
    return num_increases


if __name__ == '__main__':
    part_one_input = [int(x) for x in read_data().splitlines()]
    part_two_input = [sum(x) for x in windowed(part_one_input, 3)]
    print(f"Part one: {count_increases(part_one_input)}")
    print(f"Part two: {count_increases(part_two_input)}")
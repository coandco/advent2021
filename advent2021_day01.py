from utils import read_data
from typing import Iterable


def count_increases(data: Iterable) -> int:
    num_increases = 0
    for first, second in zip(data, data[1:]):
        if second > first:
            num_increases += 1
    return num_increases


def main():
    part_one_input = [int(x) for x in read_data().splitlines()]
    print(f"Part one: {count_increases(part_one_input)}")
    part_two_input = [sum(x) for x in zip(part_one_input, part_one_input[1:], part_one_input[2:])]
    print(f"Part two: {count_increases(part_two_input)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
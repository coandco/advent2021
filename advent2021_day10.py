from utils import read_data
from collections import deque
from statistics import median
from typing import Optional


CELL_CLOSERS = {
    "{": "}",
    "[": "]",
    "(": ")",
    "<": ">"
}

POINT_VALUES_ONE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

POINT_VALUES_TWO = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


def part_one(line: str) -> int:
    stack = deque()
    for char in line:
        if char in CELL_CLOSERS.keys():
            stack.append(CELL_CLOSERS[char])
        elif char in CELL_CLOSERS.values():
            expected_char = stack.pop()
            if char != expected_char:
                return POINT_VALUES_ONE[char]
    return 0


def part_two(line: str) -> int:
    stack = deque()
    for char in line:
        if char in CELL_CLOSERS.keys():
            stack.append(CELL_CLOSERS[char])
        elif char in CELL_CLOSERS.values():
            expected_char = stack.pop()
            if char != expected_char:
                return 0
    score = 0
    while stack:
        score *= 5
        score += POINT_VALUES_TWO[stack.pop()]
    return score


if __name__ == '__main__':
    INPUT = read_data().splitlines()
    print(f"Part one: {sum(part_one(x) for x in INPUT)}")
    part_two_data = median(points for x in INPUT if (points := part_two(x)) != 0)
    print(f"Part two: {part_two_data}")
from utils import read_data
from collections import deque
from statistics import median
from typing import NamedTuple


class PointValue(NamedTuple):
    value: int
    corrupted: bool


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


def score_line(line: str) -> PointValue:
    stack = deque()
    for char in line:
        if char in CELL_CLOSERS.keys():
            stack.append(CELL_CLOSERS[char])
        elif char in CELL_CLOSERS.values():
            expected_char = stack.pop()
            if char != expected_char:
                return PointValue(POINT_VALUES_ONE[char], corrupted=True)
    score = 0
    while stack:
        score *= 5
        score += POINT_VALUES_TWO[stack.pop()]
    return PointValue(score, corrupted=False)


if __name__ == '__main__':
    INPUT = read_data().splitlines()
    points = [score_line(x) for x in INPUT]
    print(f"Part one: {sum(x.value for x in points if x.corrupted is True)}")
    print(f"Part two: {median(x.value for x in points if x.corrupted is False)}")
from utils import read_data
from typing import Tuple, List
from math import floor, ceil
from itertools import combinations
import re

EXTRACT_DIGITS = re.compile(r'\d+')
EXTRACT_PAIRS = re.compile(r'\[\d+,\d+]')


def find_explosion(sfish_str: str) -> Tuple[bool, int, int]:
    nest_counter = 0
    for i, char in enumerate(sfish_str):
        if char == '[':
            nest_counter += 1
        elif char == ']':
            nest_counter -= 1
        if nest_counter == 5:
            return True, i, i + sfish_str[i:].index(']') + 1,
    return False, 0, 0


def do_explode(sfish_str: str, start: int, end: int) -> str:
    # Step one: extract explode str, replace it with 0, and parse the exploding components
    explode_str = sfish_str[start:end]
    sfish_str = sfish_str[:start] + '0' + sfish_str[end:]
    leftboom, rightboom = (int(x) for x in explode_str[1:-1].split(",", 1))
    # Step two: extract digits from the string and map them to their start locations so we can replace them
    digits = list(EXTRACT_DIGITS.finditer(sfish_str))
    digit_locs = {match.start(): i for i, match in enumerate(digits)}
    explode_loc = digit_locs[start]
    # Step three: replace the number to the right of the explodestr if it exists
    if explode_loc < len(digits) - 1:
        rstart, rend = digits[explode_loc+1].span()
        new_num = str(int(digits[explode_loc+1].group()) + rightboom)
        sfish_str = sfish_str[:rstart] + new_num + sfish_str[rend:]
    # Step four: replace the number to the left of the explodestr if it exists
    if explode_loc > 0:
        lstart, lend = digits[explode_loc-1].span()
        new_num = str(int(digits[explode_loc-1].group()) + leftboom)
        sfish_str = sfish_str[:lstart] + new_num + sfish_str[lend:]
    return sfish_str


def find_split(sfish_str: str) -> Tuple[bool, int, int]:
    for match in re.finditer(EXTRACT_DIGITS, sfish_str):
        if len(match.group()) > 1:
            return True, match.start(), match.end()
    return False, 0, 0


def do_split(sfish_str: str, start, end) -> str:
    num_to_split = int(sfish_str[start:end])
    left_num, right_num = floor(num_to_split/2), ceil(num_to_split/2)
    return sfish_str[:start] + f"[{left_num},{right_num}]" + sfish_str[end:]


def reduce(sfish_str: str) -> str:
    while True:
        explosion_exists, exp_start, exp_end = find_explosion(sfish_str)
        if explosion_exists:
            sfish_str = do_explode(sfish_str, exp_start, exp_end)
            continue
        split_exists, split_start, split_end = find_split(sfish_str)
        if split_exists:
            sfish_str = do_split(sfish_str, split_start, split_end)
            continue
        break

    return sfish_str


def do_add(num_one: str, num_two: str) -> str:
    return reduce(f"[{num_one},{num_two}]")


def get_magnitude(sfish_str: str) -> int:
    while pairs := list(EXTRACT_PAIRS.finditer(sfish_str))[::-1]:
        for pair in pairs:
            left, right = (int(x) for x in sfish_str[pair.start():pair.end()][1:-1].split(",", 1))
            sfish_str = sfish_str[:pair.start()] + f"{(3 * left) + (2 * right)}" + sfish_str[pair.end():]
    return int(sfish_str)


def add_all(data: List[str]) -> str:
    reversed_data = data[::-1]
    while len(reversed_data) > 1:
        num_one = reversed_data.pop()
        num_two = reversed_data.pop()
        reversed_data.append(do_add(num_one, num_two))
    return reversed_data[0]


def find_max_magnitude(data: List[str]) -> int:
    max_magnitude = 0
    for num_one, num_two in combinations(data, 2):
        max_magnitude = max(
            max_magnitude,
            get_magnitude(do_add(num_one, num_two)),
            get_magnitude(do_add(num_two, num_one))
        )
    return max_magnitude


if __name__ == '__main__':
    INPUT = read_data().splitlines()
    print(f"Part one: {get_magnitude(add_all(INPUT))}")
    print(f"Part two: {find_max_magnitude(INPUT)}")




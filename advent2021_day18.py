from utils import read_data
from typing import Tuple, List, Union
from math import floor, ceil
from itertools import combinations


SnailfishList = List[Union[int, str]]


def sfish_to_list(sfish_str: str) -> List:
    return [
        int(x) if x.isnumeric() else x
        for x in sfish_str
        if x != ','
    ]


def find_explosions(sfish_list: List) -> List[int]:
    nest_counter = 0
    explosions = []
    for i, token in enumerate(sfish_list):
        if token == '[':
            nest_counter += 1
            if nest_counter == 5:
                explosions.append(i)
        elif token == ']':
            nest_counter -= 1
    return explosions


def explode(sfish_list: SnailfishList, loc: int):
    leftboom, rightboom = sfish_list[loc + 1], sfish_list[loc + 2]
    sfish_list[loc:loc+4] = [0]
    for i in range(loc+1, len(sfish_list)):
        if isinstance(sfish_list[i], int):
            sfish_list[i] += rightboom
            break
    for i in range(loc-1, 0, -1):
        if isinstance(sfish_list[i], int):
            sfish_list[i] += leftboom
            break


def find_split(sfish_list: SnailfishList) -> int:
    for i, item in enumerate(sfish_list):
        if isinstance(item, int) and item > 9:
            return i
    return 0


def split(sfish_list: SnailfishList, loc: int):
    assert(isinstance(sfish_list[loc], int))
    sfish_list[loc:loc+1] = ['[', floor(sfish_list[loc]/2), ceil(sfish_list[loc]/2), ']']


def reduce(sfish_list: SnailfishList) -> SnailfishList:
    while True:
        loc_adjust = 0
        for explosion_loc in find_explosions(sfish_list):
            explode(sfish_list, explosion_loc+loc_adjust)
            loc_adjust -= 3
        if split_loc := find_split(sfish_list):
            split(sfish_list, split_loc)
            continue
        break
    return sfish_list


def add(list_one: SnailfishList, list_two: SnailfishList) -> SnailfishList:
    return reduce(['['] + list_one + list_two + [']'])


def add_all(data: List[SnailfishList]) -> SnailfishList:
    reversed_data = data[::-1]
    while len(reversed_data) > 1:
        num_one = reversed_data.pop()
        num_two = reversed_data.pop()
        reversed_data.append(add(num_one, num_two))
    return reversed_data[0]


def get_magnitude(sfish_list: SnailfishList) -> int:
    while pairs := list(i for i, x in enumerate(sfish_list) if x == '[' and sfish_list[i+3] == ']')[::-1]:
        for pair in pairs:
            left, right = sfish_list[pair+1], sfish_list[pair+2]
            sfish_list[pair:pair+4] = [(3 * left) + (2 * right)]
    return sfish_list[0]


def find_max_magnitude(data: List[str]) -> int:
    return max(get_magnitude(add(*x)) for x in combinations(data, 2))


if __name__ == '__main__':
    INPUT = [sfish_to_list(x) for x in read_data().splitlines()]
    print(f"Part one: {get_magnitude(add_all(INPUT))}")
    print(f"Part two: {find_max_magnitude(INPUT)}")

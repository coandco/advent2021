from utils import read_data
from typing import List


def count_column(data: List[str], column_num: int) -> int:
    count = 0
    for line in data:
        if line[column_num] == '1':
            count += 1
    return count


def part_one(data: List[str]) -> int:
    counts = [count_column(data, x) for x in range(len(data[0]))]
    gammastr = ''.join('1' if x > (len(data) // 2) else '0' for x in counts)
    epsilonstr = ''.join('1' if x == '0' else '0' for x in gammastr)
    gamma = int(f"0b{gammastr}", 2)
    epsilon = int(f"0b{epsilonstr}", 2)
    return gamma * epsilon


def part_two(data: List[str]) -> int:
    oxy_data = data.copy()
    c02_data = data.copy()
    for i in range(len(oxy_data[0])):
        if len(oxy_data) <= 1:
            break
        half = len(oxy_data) / 2
        keep_char = '1' if count_column(oxy_data, i) >= half else '0'
        oxy_data = [x for x in oxy_data if x[i] == keep_char]

    for i in range(len(c02_data[0])):
        if len(c02_data) <= 1:
            break
        half = len(c02_data) / 2
        keep_char = '0' if count_column(c02_data, i) >= half else '1'
        c02_data = [x for x in c02_data if x[i] == keep_char]

    assert(len(oxy_data) == 1)
    assert(len(c02_data) == 1)

    delta = int(f"0b{oxy_data[0]}", 2)
    epsilon = int(f"0b{c02_data[0]}", 2)

    return delta * epsilon


if __name__ == '__main__':
    INPUT = read_data().splitlines()
    print(f"Part one: {part_one(INPUT)}")
    print(f"Part two: {part_two(INPUT)}")

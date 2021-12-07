from utils import read_data
from collections import Counter


def get_cost(counts: Counter, position_to_check: int, part_two: bool = False) -> int:
    cost = 0
    for position, count in counts.items():
        distance = abs(position - position_to_check)
        if part_two:
            single_cost = distance * (distance + 1) // 2
        else:
            single_cost = distance
        cost += single_cost * count
    return cost


if __name__ == '__main__':
    INPUT = [int(x) for x in read_data().split(",")]
    counts = Counter(INPUT)
    part_one_costs = {x: get_cost(counts, x) for x in counts}
    print(f"Part one: {min(part_one_costs.values())}")
    part_two_costs = {x: get_cost(counts, x, part_two=True) for x in counts}
    print(f"Part two: {min(part_two_costs.values())}")

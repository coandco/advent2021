from utils import read_data
from collections import Counter


def get_cost(counts: Counter, position_to_check: int, part_two: bool = False) -> int:
    cost = 0
    for position, count in counts.items():
        single_cost = abs(position - position_to_check)
        if part_two:
            single_cost = single_cost * (single_cost + 1) // 2
        cost += single_cost * count
    return cost


def main():
    INPUT = [int(x) for x in read_data().split(",")]
    counts = Counter(INPUT)
    part_one_costs = {x: get_cost(counts, x) for x in range(min(counts.keys()), max(counts.keys())+1)}
    print(f"Part one: {min(part_one_costs.values())}")
    part_two_costs = {x: get_cost(counts, x, part_two=True) for x in range(min(counts.keys()), max(counts.keys())+1)}
    print(f"Part two: {min(part_two_costs.values())}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

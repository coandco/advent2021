from utils import read_data
from typing import Tuple, Dict
from collections import Counter


def run_round_countwise(rules: Dict[str, str], letters: Counter, pairs: Counter) -> Tuple[Counter, Counter]:
    new_pairs = Counter()
    for pair in pairs.keys():
        # Used to have an "if pair in rules" here, but there are no cache misses in our data
        new_pairs[pair[0] + rules[pair]] += pairs[pair]
        new_pairs[rules[pair] + pair[1]] += pairs[pair]
        letters[rules[pair]] += pairs[pair]
    return letters, new_pairs


def main():
    template, rules_str = read_data().split("\n\n", 1)
    rules = {(rule := line.split(" -> "))[0]: rule[1] for line in rules_str.splitlines()}
    letter_counts, pair_counts = Counter(template), Counter(template[x:x+2] for x in range(len(template)-1))
    for _ in range(10):
        letter_counts, pair_counts = run_round_countwise(rules, letter_counts, pair_counts)
    print(f"Part one: {max(letter_counts.values()) - min(letter_counts.values())}")
    for _ in range(30):
        letter_counts, pair_counts = run_round_countwise(rules, letter_counts, pair_counts)
    print(f"Part two: {max(letter_counts.values()) - min(letter_counts.values())}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

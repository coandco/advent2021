from utils import read_data
from typing import Tuple, Dict, Iterable
from collections import Counter


def parse_input(data: str) -> Tuple[str, Dict[str, str]]:
    template, rules_str = data.split("\n\n", 1)
    rules = {}
    for rule in rules_str.splitlines():
        rule_from, rule_to = rule.split(" -> ", 1)
        rules[rule_from] = rule_to
    return template, rules


def get_pairs(polymer: str) -> Iterable[str]:
    for i in range(len(polymer)-1):
        yield polymer[i:i+2]


def run_round_countwise(rules: Dict[str, str], letters: Counter, pairs: Counter) -> Tuple[Counter, Counter]:
    new_pairs = Counter()
    for pair in pairs.keys():
        if pair in rules:
            new_pairs[pair[0] + rules[pair]] += pairs[pair]
            new_pairs[rules[pair] + pair[1]] += pairs[pair]
            letters[rules[pair]] += pairs[pair]
    return letters, new_pairs


if __name__ == '__main__':
    template, rules = parse_input(read_data())
    letter_counts, pair_counts = Counter(template), Counter(get_pairs(template))
    for _ in range(10):
        letter_counts, pair_counts = run_round_countwise(rules, letter_counts, pair_counts)
    print(f"Part one: {max(letter_counts.values()) - min(letter_counts.values())}")
    for _ in range(30):
        letter_counts, pair_counts = run_round_countwise(rules, letter_counts, pair_counts)
    print(f"Part two: {max(letter_counts.values()) - min(letter_counts.values())}")

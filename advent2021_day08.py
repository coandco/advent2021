from utils import read_data
from typing import NamedTuple, List, FrozenSet, Dict

#  aaaa
# b    c
# b    c
#  dddd
# e    f
# e    f
#  gggg
CANONICAL_MAPPINGS = {
    frozenset("cf"): "1",
    frozenset("acf"): "7",
    frozenset("bcdf"): "4",
    frozenset("acdeg"): "2",
    frozenset("acdfg"): "3",
    frozenset("abdfg"): "5",
    frozenset("abdefg"): "6",
    frozenset("abcdfg"): "9",
    frozenset("abcefg"): "0",
    frozenset("abcdefg"): "8"
}


def get_single_set_value(myset: FrozenSet) -> str:
    assert(len(myset) == 1)
    return next(iter(myset))


class Line(NamedTuple):
    input: List[FrozenSet[str]]
    output: List[str]

    @staticmethod
    def from_str(line: str) -> 'Line':
        inputs, outputs = line.split(" | ", 1)
        return Line(input=inputs.split(" "), output=outputs.split(" "))

    def count_part_one(self) -> int:
        total = 0
        for output in self.output:
            # 1 has 2 segments, 7 has 3, 4 has 4, and 8 has 7
            if len(output) in (2, 3, 4, 7):
                total += 1
        return total

    def get_input_of_length(self, length: int) -> List[FrozenSet[str]]:
        return [frozenset(x) for x in self.input if len(x) == length]

    def make_mappings(self) -> Dict[str, str]:
        known_mappings = {}
        c_f_set = self.get_input_of_length(2)[0]
        a_c_f_set = self.get_input_of_length(3)[0]
        known_mappings["a"] = get_single_set_value(a_c_f_set - c_f_set)
        a_b_f_g_set = frozenset.intersection(*self.get_input_of_length(6))
        c_d_e_set = frozenset.union(*(x - a_b_f_g_set for x in self.get_input_of_length(6)))
        known_mappings["c"] = get_single_set_value(c_d_e_set & c_f_set)
        known_mappings["f"] = get_single_set_value(c_f_set - {known_mappings["c"]})
        d_e_set = c_d_e_set - {known_mappings["c"]}
        b_d_set = self.get_input_of_length(4)[0] - {known_mappings["c"]} - {known_mappings["f"]}
        known_mappings["d"] = get_single_set_value(d_e_set & b_d_set)
        known_mappings["e"] = get_single_set_value(c_d_e_set - {known_mappings["c"]} - {known_mappings["d"]})
        d_g_set = frozenset.intersection(*self.get_input_of_length(5)) - {known_mappings["a"]}
        known_mappings["d"] = get_single_set_value(d_g_set & b_d_set)
        known_mappings["g"] = get_single_set_value(d_g_set - {known_mappings["d"]})
        known_mappings["b"] = get_single_set_value(b_d_set - {known_mappings["d"]})
        return {v: k for k, v in known_mappings.items()}

    def parse_output(self) -> int:
        mappings = self.make_mappings()
        real_output = ""
        for output_str in self.output:
            real_set = frozenset(output_str.translate(str.maketrans(mappings)))
            real_output += CANONICAL_MAPPINGS[real_set]
        return int(real_output)


INPUT = [Line.from_str(x) for x in read_data().splitlines()]
print(f"Part one: {sum([x.count_part_one() for x in INPUT])}")
print(f"Part two: {sum([x.parse_output() for x in INPUT])}")

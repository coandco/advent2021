from utils import read_data
from typing import List
from math import prod

LTYPE_BITS = 0
LTYPE_PACKETS = 1
OTYPE_SUM = 0
OTYPE_PROD = 1
OTYPE_MIN = 2
OTYPE_MAX = 3
OTYPE_LITERAL = 4
OTYPE_GT = 5
OTYPE_LT = 6
OTYPE_EQ = 7


class Packet:
    version: int
    type: int
    length_type: int
    length: int
    sub_packets: List['Packet']
    value: int
    unused: str

    def __init__(self, binstr: str):
        self.version, rest = int(binstr[:3], 2), binstr[3:]
        self.type, rest = int(rest[:3], 2), rest[3:]
        if self.type == OTYPE_LITERAL:
            self.length_type = 0
            self.length = 0
            self.sub_packets = []
            value_str = ''
            while True:
                more_chunks, chunk, rest = int(rest[0]), rest[1:5], rest[5:]
                value_str += chunk
                if not more_chunks:
                    break
            self.value = int(value_str, 2)
        else:
            # If it's not a literal value, it's an operator
            self.length_type, rest = int(rest[0]), rest[1:]
            self.length, rest = (int(rest[:11], 2), rest[11:]) if self.length_type else (int(rest[:15], 2), rest[15:])
            self.sub_packets = []
            if self.length_type == LTYPE_BITS:
                raw_subpackets, rest = rest[:self.length], rest[self.length:]
                while raw_subpackets:
                    new_subpacket = Packet(raw_subpackets)
                    self.sub_packets.append(new_subpacket)
                    raw_subpackets = new_subpacket.unused
            elif self.length_type == LTYPE_PACKETS:
                for _ in range(self.length):
                    new_subpacket = Packet(rest)
                    self.sub_packets.append(new_subpacket)
                    rest = new_subpacket.unused
        self.unused = rest

    def sum_versions(self):
        return self.version + sum(x.sum_versions() for x in self.sub_packets)

    def get_value(self):
        sub_values = [x.get_value() for x in self.sub_packets]
        if self.type == OTYPE_SUM:
            return sum(sub_values)
        elif self.type == OTYPE_PROD:
            return prod(sub_values)
        elif self.type == OTYPE_MIN:
            return min(sub_values)
        elif self.type == OTYPE_MAX:
            return max(sub_values)
        elif self.type == OTYPE_LITERAL:
            return self.value
        elif self.type == OTYPE_GT:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self.type == OTYPE_LT:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self.type == OTYPE_EQ:
            return 1 if sub_values[0] == sub_values[1] else 0
        raise Exception("Unknown type!")


def main():
    INPUT = f"{int(read_data(), 16):0{len(read_data())*4}b}"
    packet = Packet(INPUT)
    print(f"Part one: {packet.sum_versions()}")
    print(f"Part two: {packet.get_value()}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

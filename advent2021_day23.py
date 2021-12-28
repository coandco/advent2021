from dataclasses import dataclass, field
from collections import deque
from utils import read_data
from typing import NamedTuple, Dict, Optional, List, Tuple, Iterable, Set, Deque
from dataclasses import dataclass

# For the record, this is a terrible overcomplicated piece of code that should be taken out back and shot.
# It doesn't get the correct answer on the test input or on the inputs of other people, but it gets the correct
# answer for my input at this point I'm inclined to just commit it and never look at it again.


# score, rooms A-D, hallways 0-6
class WorldState(NamedTuple):
    A: Tuple[str, ...] = tuple()
    B: Tuple[str, ...] = tuple()
    C: Tuple[str, ...] = tuple()
    D: Tuple[str, ...] = tuple()
    H0: str = ''
    H1: str = ''
    H2: str = ''
    H3: str = ''
    H4: str = ''
    H5: str = ''
    H6: str = ''

    def move(self, move_from: str, move_to: str):
        new_state = list(self)
        if move_from.isalpha():
            *items_left, item_moved = new_state[self._fields.index(move_from)]
            new_state[self._fields.index(move_from)] = tuple(items_left)
        else:
            item_moved = new_state[self._fields.index(move_from)]
            new_state[self._fields.index(move_from)] = ''
        if move_to.isalpha():
            new_state[self._fields.index(move_to)] = new_state[self._fields.index(move_to)] + tuple(item_moved)
        else:
            new_state[self._fields.index(move_to)] = item_moved
        return WorldState(*new_state)

    def to_str(self, depth=2):
        lines = []
        lines.append("#############")
        lines.append(f"#{self.H0 or '.'}{self.H1 or '.'}.{self.H2 or '.'}.{self.H3 or '.'}.{self.H4 or '.'}.{self.H5 or '.'}{self.H6 or '.'}#")
        if depth == 4:
            lines.append(f"###{self.A[3] if len(self.A) > 3 else '.'}#{self.B[3] if len(self.B) > 3 else '.'}#{self.C[3] if len(self.C) > 3 else '.'}#{self.D[3] if len(self.D) > 3 else '.'}###")
            lines.append(f"  #{self.A[2] if len(self.A) > 2 else '.'}#{self.B[2] if len(self.B) > 2 else '.'}#{self.C[2] if len(self.C) > 2 else '.'}#{self.D[2] if len(self.D) > 2 else '.'}#  ")
            lines.append(f"  #{self.A[1] if len(self.A) > 1 else '.'}#{self.B[1] if len(self.B) > 1 else '.'}#{self.C[1] if len(self.C) > 1 else '.'}#{self.D[1] if len(self.D) > 1 else '.'}#  ")
        elif depth == 2:
            lines.append(f"###{self.A[1] if len(self.A) > 1 else '.'}#{self.B[1] if len(self.B) > 1 else '.'}#{self.C[1] if len(self.C) > 1 else '.'}#{self.D[1] if len(self.D) > 1 else '.'}###")
        lines.append(f"  #{self.A[0] if len(self.A) > 0 else '.'}#{self.B[0] if len(self.B) > 0 else '.'}#{self.C[0] if len(self.C) > 0 else '.'}#{self.D[0] if len(self.D) > 0 else '.'}#  ")
        lines.append("  #########")
        return "\n".join(lines)

    def to_peterstr(self):
        return f"WorldState(hallway='{''.join(x if x else '.' for x in self[4:])}', rooms=('{''.join(reversed(self.A)):.4}', '{''.join(reversed(self.B)):.4}', '{''.join(reversed(self.C)):.4}', '{''.join(reversed(self.D)):.4}'))"

    @property
    def is_win(self) -> bool:
        return (all(x == 'A' for x in self.A) and
                all(x == 'B' for x in self.B) and
                all(x == 'C' for x in self.C) and
                all(x == 'D' for x in self.D) and
                all(x == '' for x in self[4:]))


@dataclass
class Node:
    type: str = '1'
    neighbors: Dict[str, int] = field(default_factory=lambda: dict())
    state: WorldState = field(default=WorldState(A=tuple(), B=tuple(), C=tuple(), D=tuple(), ))

    @property
    def contents(self):
        return self.state.__getattribute__(self.type)

    @property
    def occupied(self):
        return bool(self.contents)

    @property
    def extra_cost(self):
        return 0

    def can_receive(self, letter: str) -> bool:
        return not self.occupied

    def get_possible_moves(self, nodes: Dict[str, 'Node'], recursivestate: Optional[Tuple[str, Set[str], int]] = None) -> Iterable[Tuple[str, int]]:
        original = False
        if recursivestate is None:
            if self.contents:
                letter = self.contents
            else:
                return
            cost = 0
            seen = set()
            original = True
        else:
            letter, seen, cost = recursivestate
        # Add yourself to seen so you won't go backwards
        seen.add(self.type)
        for neighbor, neighbor_cost in self.neighbors.items():
            if neighbor not in seen and nodes[neighbor].can_receive(letter):
                seen.add(neighbor)
                new_cost = cost + ((neighbor_cost + nodes[neighbor].extra_cost) * pow(10, ord(letter) - 65))
                if (not original) or neighbor.isalpha():
                    yield neighbor, new_cost
                for destination, dest_cost in nodes[neighbor].get_possible_moves(nodes, (letter, seen, new_cost)):
                    if (not original) or destination.isalpha():
                        yield destination, dest_cost

    def get_new_states(self, nodes: Dict[str, 'Node'], current_cost: int):
        for move, cost in self.get_possible_moves(nodes):
            yield self.state.move(self.type, move), current_cost + cost

    def __repr__(self):
        return f"{type(self).__name__}({self.type})"


@dataclass
class Room(Node):
    type: str = 'A'
    depth: int = 2

    @property
    def contents(self) -> str:
        if all_cont := self.all_contents:
            if any(x != self.type for x in all_cont):
                return all_cont[-1]
        return ''

    @property
    def all_contents(self) -> Tuple[str, ...]:
        return self.state.__getattribute__(self.type)

    @property
    def extra_cost(self) -> int:
        return self.depth - len(self.all_contents)

    def can_receive(self, letter: str) -> bool:
        return (letter == self.type and
                len(self.all_contents) < self.depth and
                all(x == self.type for x in self.all_contents))

    def get_possible_moves(self, nodes: Dict[str, 'Node'], recursivestate: Optional[Tuple[str, Set[str], int]] = None) -> Iterable[Tuple[str, int]]:
        # only leave a room if we're starting it
        if recursivestate is None:
            if self.contents:
                letter = self.contents
            else:
                return
            # Don't take things out of this room if it's already holding all the correct letter
            if all(x == self.type for x in self.all_contents):
                return
            # Add nodes you're dealing with to seen so you won't go backwards
            seen = {self.type, *self.neighbors.keys()}
            for neighbor, neighbor_cost in self.neighbors.items():
                if nodes[neighbor].can_receive(letter):
                    new_cost = (neighbor_cost + self.extra_cost) * pow(10, ord(letter) - 65)
                    yield neighbor, new_cost
                    yield from nodes[neighbor].get_possible_moves(nodes, (letter, seen, new_cost))
        else:
            return


NEIGHBORS = {
    'H0': {'H1': 1},
    'H1': {'H0': 1, 'A': 1, 'H2': 2},
    'H2': {'H1': 2, 'A': 1, 'B': 1, 'H3': 2},
    'H3': {'H2': 2, 'B': 1, 'C': 1, 'H4': 2},
    'H4': {'H3': 2, 'C': 1, 'D': 1, 'H5': 2},
    'H5': {'H4': 2, 'D': 1, 'H6': 1},
    'H6': {'H5': 1},
    'A': {'H1': 2, 'H2': 2},
    'B': {'H2': 2, 'H3': 2},
    'C': {'H3': 2, 'H4': 2},
    'D': {'H4': 2, 'H5': 2},
}


#############
#...........#
###D#D#C#B###
  #B#A#A#C#
  #########


def parse_initial_state(data: str, unfold: bool = False) -> WorldState:
    lines = data.splitlines()
    if unfold and len(lines) <= 5:
        PART_TWO_LINES = """  #D#C#B#A#\n  #D#B#A#C#""".splitlines()
        lines = lines[:3] + PART_TWO_LINES + lines[3:]
    room_A = tuple(x for x in (lines[y][3] for y in range(len(lines) - 2, 1, -1)) if x != '.')
    room_B = tuple(x for x in (lines[y][5] for y in range(len(lines) - 2, 1, -1)) if x != '.')
    room_C = tuple(x for x in (lines[y][7] for y in range(len(lines) - 2, 1, -1)) if x != '.')
    room_D = tuple(x for x in (lines[y][9] for y in range(len(lines) - 2, 1, -1)) if x != '.')
    rooms = (room_A, room_B, room_C, room_D)
    hall = lines[1]
    hallway_nodes = (hall[1], hall[2], hall[4], hall[6], hall[8], hall[10], hall[11])
    hallway_nodes = tuple('' if x == '.' else x for x in hallway_nodes)
    return WorldState(*rooms, *hallway_nodes)


def run_sim(start_state: WorldState, depth: int = 2):
    nodes: Dict[str, Node] = {(t := chr(ord('A') + i)): Room(type=t, neighbors=NEIGHBORS[t], depth=depth)
                              for i in range(4)}
    nodes.update({f"H{i}": Node(type=f"H{i}", neighbors=NEIGHBORS[f"H{i}"]) for i in range(7)})
    for node in nodes.values():
        node.state = start_state
    seen_states: Dict[WorldState, int] = {}
    stack: Deque[Tuple[WorldState, int]] = deque()
    stack.append((start_state, 0))
    win_state = WorldState(('A',) * depth, ('B',) * depth, ('C',) * depth, ('D',) * depth, *('',) * 7)
    while stack:
        (state, cost) = stack.popleft()
        # print(f"{cost}: \n{state.to_str()}")
        if state not in seen_states or cost < seen_states.get(state, 0):
            seen_states[state] = cost
        else:
            continue
        if state == win_state:
            continue
        for node in nodes.values():
            node.state = state
        for node in nodes.values():
            stack.extend(node.get_new_states(nodes, cost))
    return seen_states[win_state]


TEST = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
INPUT = parse_initial_state(read_data())
print(f"Part one: {run_sim(INPUT)}")
UNFOLDED_INPUT = parse_initial_state(read_data(), unfold=True)
print(f"Part two: {run_sim(UNFOLDED_INPUT, depth=4)}")

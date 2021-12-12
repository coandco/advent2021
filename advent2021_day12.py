from utils import read_data
from typing import List, Dict, Set
from collections import deque


class Cave:
    name: str
    connections: Set[str]

    def __init__(self, name: str):
        self.name = name
        self.connections = set()

    def add_connection(self, other: str):
        self.connections.add(other)

    def __repr__(self):
        return f"Cave({self.name})"


def process_input(data: List[str]) -> Dict[str, Cave]:
    caves: Dict[str, Cave] = {}
    for line in data:
        first_name, second_name = line.split("-", 1)
        caves[first_name] = caves.get(first_name, Cave(first_name))
        caves[second_name] = caves.get(second_name, Cave(second_name))
        caves[first_name].add_connection(second_name)
        caves[second_name].add_connection(first_name)
    return caves


def build_paths(caves: Dict[str, Cave], visit_twice: bool = False) -> int:
    paths = 0
    path_queue = deque()
    path_queue.append(("start", frozenset(["start"]), not visit_twice))
    while path_queue:
        current_location, items_in_path, extra_visit_used = path_queue.pop()
        if current_location == "end":
            paths += 1
            continue
        for connection in caves[current_location].connections:
            if connection == 'start' or (connection.islower() and extra_visit_used and connection in items_in_path):
                continue
            if extra_visit_used is False and connection.islower():
                extra_visit_will_be_used = connection in items_in_path
            else:
                extra_visit_will_be_used = extra_visit_used
            path_queue.append((connection, items_in_path | {connection}, extra_visit_will_be_used))
    return paths


if __name__ == '__main__':
    caves = process_input(read_data().splitlines())
    print(f"Part one: {build_paths(caves, visit_twice=False)}")
    print(f"Part two: {build_paths(caves, visit_twice=True)}")


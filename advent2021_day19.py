from utils import read_data
from typing import FrozenSet, NamedTuple, Tuple, Dict, List
from itertools import combinations


TRANSFORMATIONS = [
    ('x', 'y', 'z'),
    ('x', 'z', '-y'),
    ('x', '-y', '-z'),
    ('x', '-z', 'y'),
    ('y', 'x', '-z'),
    ('y', 'z', 'x'),
    ('y', '-x', 'z'),
    ('y', '-z', '-x'),
    ('z', 'x', 'y'),
    ('z', 'y', '-x'),
    ('z', '-x', '-y'),
    ('z', '-y', 'x'),
    ('-x', 'y', '-z'),
    ('-x', 'z', 'y'),
    ('-x', '-y', 'z'),
    ('-x', '-z', '-y'),
    ('-y', 'x', 'z'),
    ('-y', 'z', '-x'),
    ('-y', '-x', '-z'),
    ('-y', '-z', 'x'),
    ('-z', 'x', '-y'),
    ('-z', 'y', 'x'),
    ('-z', '-x', 'y'),
    ('-z', '-y', '-x')
]


class Coord3D(NamedTuple):
    x: int
    y: int
    z: int

    def distance(self, other: 'Coord3D') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def anondelta(self, other: 'Coord3D') -> FrozenSet[int]:
        return frozenset((abs(self.x-other.x), abs(self.y-other.y), abs(self.z-other.z)))

    def transform(self, tx: str, ty: str, tz: str) -> 'Coord3D':
        x = getattr(self, tx[-1]) if len(tx) == 1 else -1 * getattr(self, tx[-1])
        y = getattr(self, ty[-1]) if len(ty) == 1 else -1 * getattr(self, ty[-1])
        z = getattr(self, tz[-1]) if len(tz) == 1 else -1 * getattr(self, tz[-1])
        return Coord3D(x=x, y=y, z=z)

    def __add__(self, other):
        return Coord3D(x=self.x+other.x, y=self.y+other.y, z=self.z+other.z)

    def __sub__(self, other):
        return Coord3D(x=self.x-other.x, y=self.y-other.y, z=self.z-other.z)


    @staticmethod
    def from_str(coords_str: str) -> 'Coord3D':
        return Coord3D(*(int(x) for x in coords_str.split(",", 2)))


class Scanner:
    name: str
    points: List[Coord3D]
    deltas: Dict[Coord3D, Tuple[Coord3D, Coord3D]]
    anon_deltas: Dict[FrozenSet[int], Tuple[Coord3D, Coord3D]]
    offset: Coord3D

    def __init__(self, raw: str):
        self.name, *rawpoints = raw.splitlines()
        self.points = [Coord3D(*[int(p) for p in x.split(",")]) for x in rawpoints]
        self.anon_deltas = {x.anondelta(y): (x, y) for x, y in combinations(self.points, 2)}
        self.offset = Coord3D(0, 0, 0)

    def rectify(self, other: 'Scanner') -> bool:
        anon_overlap_hash = next(iter(set(self.anon_deltas) & set(other.anon_deltas)))
        for transformation in TRANSFORMATIONS:
            transformed_points = [x.transform(*transformation) for x in self.points]

            other_point = other.anon_deltas[anon_overlap_hash][0]
            for self_point in self.anon_deltas[anon_overlap_hash]:
                transformed_point = self_point.transform(*transformation)
                diff = other_point - transformed_point
                diffed_points = [x + diff for x in transformed_points]
                if len(set(diffed_points) & set(other.points)) >= 12:
                    self.offset = diff
                    self.points = diffed_points
                    self.anon_deltas = {x.anondelta(y): (x, y) for x, y in combinations(diffed_points, 2)}
                    return True
        return False

    def __repr__(self):
        return f"Scanner({self.name})"

    def __hash__(self):
        return hash(self.__repr__())


def main():
    scanners = [Scanner(x) for x in read_data().split("\n\n")]
    known_scanners = newly_known = [scanners[0]]
    unknown_scanners = scanners[1:]

    while unknown_scanners:
        assert len(newly_known) > 0
        to_check = newly_known[:]
        newly_known = []
        for known_scanner in to_check:
            matches = {x for x in unknown_scanners if len(set(known_scanner.anon_deltas) & set(x.anon_deltas)) >= 66}
            still_unknown = []
            for unknown_scanner in unknown_scanners:
                if unknown_scanner in matches and unknown_scanner.rectify(known_scanner):
                    newly_known.append(unknown_scanner)
                else:
                    still_unknown.append(unknown_scanner)
            unknown_scanners = still_unknown
        known_scanners.extend(newly_known)

    all_points = set.union(*(set(x.points) for x in known_scanners))
    print(f"Part one: {len(all_points)}")
    offsets = [x.offset for x in known_scanners]
    max_distance = max(x.distance(y) for x, y in combinations(offsets, 2))
    print(f"Part two: {max_distance}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

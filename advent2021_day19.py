from utils import read_data
from typing import FrozenSet, NamedTuple, Tuple, Dict, List
from itertools import combinations, permutations, product
from pathlib import Path


# TRANSFORMATIONS = [
#     ('x',  'y',  'z'),
#     ('x',  '-z', 'y'),
#     ('x',  '-y', '-z'),
#     ('x',  'z',  '-y'),
#     ('-y', 'x',  'z'),
#     ('z',  'x',  'y'),
#     ('y',  'x',  '-z'),
#     ('-z', 'x',  '-y'),
#     ('-x', '-y', 'z'),
#     ('-x', '-z', '-y'),
#     ('-x', 'y',  '-z'),
#     ('-x', 'z',  'y'),
#     ('y',  '-x', 'z'),
#     ('z',  '-x', '-y'),
#     ('-y', '-x', '-z'),
#     ('-z', '-y', 'x'),
#     ('-z', 'y',  'x'),
#     ('y',  'z',  'x'),
#     ('z',  '-y', 'x'),
#     ('-y', '-z', 'x'),
#     ('-z', '-y', '-x'),
#     ('-y', 'z',  '-x'),
#     ('z',  'y',  '-x'),
#     ('y',  '-z', '-x')
# ]

TRANSFORMATIONS = []
for X_perm in permutations(["x", "y", "z"]):
    for X_muls in product([-1, 1], [-1, 1], [-1, 1]):
        print(X_muls)
        TRANSFORMATIONS.append((
            ("" if X_muls[0] < 0 else "-") + X_perm[0],
            ("" if X_muls[1] < 0 else "-") + X_perm[1],
            ("" if X_muls[2] < 0 else "-") + X_perm[2],
        ))


TEST = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


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


if __name__ == '__main__':
    INPUT = [Scanner(x) for x in read_data().split("\n\n")]
    known_scanners = newly_known = [INPUT[0]]
    unknown_scanners = INPUT[1:]

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
                    print(f"Added {unknown_scanner.name}")
                else:
                    still_unknown.append(unknown_scanner)
            unknown_scanners = still_unknown
        known_scanners.extend(newly_known)

    all_points = set.union(*(set(x.points) for x in known_scanners))
    print(f"Part one: {len(all_points)}")
    offsets = [x.offset for x in known_scanners]
    max_distance = max(x.distance(y) for x, y in combinations(offsets, 2))
    print(f"Part two: {max_distance}")

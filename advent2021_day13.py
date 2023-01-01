from utils import read_data
import sys
from typing import NamedTuple, List, Tuple, Set


class Coord(NamedTuple):
    x: int
    y: int


class Fold(NamedTuple):
    axis: str
    at: int


# Taken from the advent-of-code-ocr package
ALPHABET_6 = {
    " ## \n#  #\n#  #\n####\n#  #\n#  #": "A",
    "### \n#  #\n### \n#  #\n#  #\n### ": "B",
    " ## \n#  #\n#   \n#   \n#  #\n ## ": "C",
    "####\n#   \n### \n#   \n#   \n####": "E",
    "####\n#   \n### \n#   \n#   \n#   ": "F",
    " ## \n#  #\n#   \n# ##\n#  #\n ###": "G",
    "#  #\n#  #\n####\n#  #\n#  #\n#  #": "H",
    " ###\n  # \n  # \n  # \n  # \n ###": "I",
    "  ##\n   #\n   #\n   #\n#  #\n ## ": "J",
    "#  #\n# # \n##  \n# # \n# # \n#  #": "K",
    "#   \n#   \n#   \n#   \n#   \n####": "L",
    " ## \n#  #\n#  #\n#  #\n#  #\n ## ": "O",
    "### \n#  #\n#  #\n### \n#   \n#   ": "P",
    "### \n#  #\n#  #\n### \n# # \n#  #": "R",
    " ###\n#   \n#   \n ## \n   #\n### ": "S",
    "#  #\n#  #\n#  #\n#  #\n#  #\n ## ": "U",
    "#   \n#   \n # #\n  # \n  # \n  # ": "Y",
    "####\n   #\n  # \n #  \n#   \n####": "Z",
}


# Also adapted from advent-of-code-ocr
def parse_output(raw: str) -> str:
    lines = raw.splitlines()
    line_length = len(lines[0])
    parsed_output = ""
    low, high = 0, 4
    while high <= line_length:
        single_letter = ALPHABET_6["\n".join([x[low:high] for x in lines])]
        parsed_output += single_letter
        low += 5
        high += 5
    return parsed_output


def parse_input(data: str) -> Tuple[Set[Coord], List[Fold]]:
    coord_str, folds_str = data.split("\n\n", 1)
    coords = set()
    for line in coord_str.splitlines():
        coords.add(Coord(*(int(x) for x in line.split(","))))
    folds = []
    for line in folds_str.splitlines():
        # Drop the unnecessary stuff before the last space
        line = line.rsplit(" ", 1)[-1]
        axis, at = line.split("=", 1)
        folds.append(Fold(axis, int(at)))
    return coords, folds


def do_fold(dots: Set[Coord], fold: Fold) -> Set[Coord]:
    newdots = dots.copy()
    if fold.axis == 'x':
        dots_to_fold = [x for x in newdots if x.x > fold.at]
        for dot in dots_to_fold:
            newdots.remove(dot)
            newdots.add(Coord(x=dot.x - 2 * (dot.x - fold.at), y=dot.y))
    else:
        dots_to_fold = [x for x in newdots if x.y > fold.at]
        for dot in dots_to_fold:
            newdots.remove(dot)
            newdots.add(Coord(x=dot.x, y=dot.y - 2 * (dot.y - fold.at)))
    return newdots


def output_dots(dots: Set[Coord]):
    min_x = min_y = sys.maxsize
    max_x = max_y = 0
    for dot in dots:
        min_x = dot.x if dot.x < min_x else min_x
        max_x = dot.x if dot.x > max_x else max_x
        min_y = dot.y if dot.y < min_y else min_y
        max_y = dot.y if dot.y > max_y else max_y
    output = []
    for y in range(min_y, max_y+1):
        line = "".join("#" if Coord(x=x, y=y) in dots else " " for x in range(min_x, max_x+1))
        output.append(line)
    return "\n".join(output)


def main():
    dots, folds = parse_input(read_data())
    part_one_dots = do_fold(dots, folds[0])
    print(f"Part one: {len(part_one_dots)}")
    for fold in folds:
        dots = do_fold(dots, fold)
    print(f"Part two: {parse_output(output_dots(dots))}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

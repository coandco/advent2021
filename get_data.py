from aocd.models import Puzzle
from pathlib import Path

# This is a standalone script meant to be run to automatically grab my data
# for a given year/day and dump it into an automatically-named file.

YEAR_NUM = 2021
DAY_NUM = 1

puzzle = Puzzle(year=YEAR_NUM, day=DAY_NUM)

file_location = Path(f'inputs/advent{YEAR_NUM}_day{DAY_NUM:02d}_input.txt')
file_location.write_text(puzzle.input_data)

program_location = Path(f"advent{YEAR_NUM}_day{DAY_NUM:02d}.py")
if not program_location.exists():
    program_location.write_text("from utils import read_data")
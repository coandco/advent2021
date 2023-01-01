from typing import List, Tuple
from utils import read_data
from math import floor


def parse_input(data: str) -> List[Tuple[int, int, int]]:
    digits = []
    for program in filter(None, data.split("inp w\n")):
        _, program = program.split("\nmod x 26\n", 1)
        part_one, part_two = program.split("\nadd y w\n", 1)
        part_one = part_one.splitlines()
        div_z = int(part_one[0].split()[-1])
        add_x = int(part_one[1].split()[-1])
        add_y = int(part_two.splitlines()[0].split()[-1])
        digits.append((div_z, add_x, add_y))
    return digits


def run_iteration(check_vals: Tuple[int, int, int], digit: int, old_z: int):
    div_z, add_x, add_y = check_vals
    x = (old_z % 26) + add_x
    z = floor(old_z / div_z)
    if x != digit:
        z *= 26
        z += digit + add_y
    return z


def recursive_check(check_vals: List[Tuple[int, int, int]], reverse: bool = False, z: int = 0, i: int = 0) -> str:
    div_z, add_x, _ = check_vals[i]
    if div_z > 1:
        allowed_digit = (z % 26) + add_x
        if 1 <= allowed_digit <= 9:
            new_z = run_iteration(check_vals[i], allowed_digit, z)
            if i < 13:
                rest_of_number = recursive_check(check_vals, reverse, new_z, i+1)
                if rest_of_number:
                    return str(allowed_digit) + rest_of_number
            return str(allowed_digit) if new_z == 0 else ''
    else:
        digits_to_try = range(1, 10) if reverse else range(9, 0, -1)
        for possible_digit in digits_to_try:
            possible_z = run_iteration(check_vals[i], possible_digit, z)
            rest_of_number = recursive_check(check_vals, reverse, possible_z, i+1)
            if rest_of_number:
                return str(possible_digit) + rest_of_number
    # If we hit a dead end, return an empty/falsey string to cut this branch off
    return ''


# Keeping this transliteration around for archival purposes, even though I don't actually use it
def run_check_raw(check_vals: List[Tuple[int, int, int]], to_check: str) -> bool:
    w = x = y = z = 0
    assert len(to_check) == 14
    for i, digit in enumerate(to_check):
        div_z, add_x, add_y = check_vals[i]
        w = int(digit)
        x *= 0
        x += z
        x %= 26
        z = floor(z / div_z)
        x += add_x
        x = 1 if x == w else 0
        x = 1 if x == 0 else 0
        y *= 0
        y += 25
        y *= x
        y += 1
        z *= y
        y *= 0
        y += w
        y += add_y
        y *= x
        z += y
        print(f"raw: digit {digit} has z value {z}")

    return z == 0


def main():
    digits = parse_input(read_data())
    print(f"Part one: {recursive_check(digits)}")
    print(f"Part two: {recursive_check(digits, reverse=True)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

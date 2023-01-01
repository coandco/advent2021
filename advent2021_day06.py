from utils import read_data
from collections import Counter


def run_cycle(current_state: Counter) -> Counter:
    new_state = Counter()
    for i in range(1, 9):
        new_state[i-1] = current_state.get(i, 0)
    new_state[6] += current_state[0]
    new_state[8] = current_state[0]
    return new_state


def main():
    INPUT = [int(x) for x in read_data().split(",")]
    state = Counter(INPUT)
    for _ in range(80):
        state = run_cycle(state)
    print(f"Part one: {sum(state.values())}")

    state = Counter(INPUT)
    for _ in range(256):
        state = run_cycle(state)
    print(f"Part two: {sum(state.values())}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

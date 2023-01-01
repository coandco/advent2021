from utils import read_data
from typing import Generator, List, Tuple, Dict, Optional
from collections import defaultdict


# WorldState: player_locs, player_scores, turn_index
WorldState = Tuple[Tuple[int, int], Tuple[int, int]]


def fixed_die(start: int = 1, sides: int = 100) -> Generator[int, None, None]:
    while True:
        yield from range(start, sides+1)


def mutate(state: WorldState, roll: int) -> WorldState:
    locs, scores = state

    new_loc = (locs[0] + roll) % 10
    # We add one to the score because we're mapping spots 1-10 onto 0-9 so we can do modulo on them
    new_score = scores[0] + new_loc + 1
    return (locs[1], new_loc), (scores[1], new_score)


def state_winner(state: WorldState, limit: int = 21) -> Optional[int]:
    _, scores = state
    for i, score in enumerate(scores):
        if score >= limit:
            return i
    return None


def part_one(starting_locs: List[int]) -> int:
    # state: player_locs, player_scores, turn_index
    state: WorldState = ((starting_locs[0], starting_locs[1]), (0, 0))
    die = fixed_die()
    num_rolls = 0
    while (winner := state_winner(state, limit=1000)) is None:
        state = mutate(state, next(die) + next(die) + next(die))
        num_rolls += 3
    return state[1][not winner] * num_rolls


# Roll distribution for three rolls of the quantum die.
# Each time the three quantum dice are rolled, it creates 27 new universes.  However, the
# universes where the rolls add up to the same number are indistinguishable -- thus, universes
# where it rolls 1+2+3 are the same as the universes where it rolls 3+2+1.  We can therefore
# generate a static dict of the number of universes for each roll total via the following method:
# ROLLS = {}
# for x in range(1, 4):
#     for y in range(1, 4):
#         for z in range(1, 4):
#             ROLLS[x+y+z] = ROLLS.get(x+y+z, 0) + 1
ROLLS = {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}


def part_two(starting_locs: List[int]) -> int:
    states: Dict[WorldState, int] = {((starting_locs[0], starting_locs[1]), (0, 0)): 1}
    winning_states: List[int] = [0, 0]

    while states:
        # Python dicts are ordered since 3.5, and this will get the first-inserted item from the dict and delete it
        new_states = defaultdict(int)
        for state, universes in states.items():
            if (winner := state_winner(state, limit=21)) is not None:
                winning_states[winner] += universes
                continue

            for roll, roll_universes in ROLLS.items():
                new_state = mutate(state, roll)
                new_states[new_state] += universes * roll_universes
        winning_states[0], winning_states[1] = winning_states[1], winning_states[0]
        states = new_states
    return max(winning_states)


def main():
    # It's convenient to have the player locs be 0-9 instead of 1-10 so modulo works
    player_locs = [int(x[-2:].strip())-1 for x in read_data().splitlines()]
    print(f"Part one: {part_one(player_locs)}")
    print(f"Part two: {part_two(player_locs)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

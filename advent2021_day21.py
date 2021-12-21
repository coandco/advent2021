from utils import read_data
from typing import Generator, List, Tuple, Dict, Optional


# WorldState: player_locs, player_scores, turn_index
WorldState = Tuple[Tuple[int, int], Tuple[int, int], int]


def fixed_die(start: int = 1, sides: int = 100) -> Generator[int, None, None]:
    while True:
        yield from range(start, sides+1)


def mutate(state: WorldState, roll: int) -> WorldState:
    locs, scores, pnum = state

    new_loc = (locs[pnum] + roll) % 10
    # We add one to the score because we're mapping spots 1-10 onto 0-9 so we can do modulo on them
    new_score = scores[pnum] + new_loc + 1
    if pnum:
        return (locs[not pnum], new_loc), (scores[not pnum], new_score), int(not pnum)
    else:
        return (new_loc, locs[not pnum]), (new_score, scores[not pnum]), int(not pnum)


def state_winner(state: WorldState, limit: int = 21) -> Optional[int]:
    _, scores, _ = state
    for i, score in enumerate(scores):
        if score >= limit:
            return i
    return None


def part_one(starting_locs: List[int]) -> int:
    # state: player_locs, player_scores, turn_index
    state: WorldState = ((starting_locs[0], starting_locs[1]), (0, 0), 0)
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
    states: Dict[WorldState, int] = {((starting_locs[0], starting_locs[1]), (0, 0), 0): 1}
    winning_states: List[int] = [0, 0]

    while states:
        # Python dicts are ordered since 3.5, and this will get the first-inserted item from the dict and delete it
        state, universes = next(iter(states.items()))
        del states[state]

        if (winner := state_winner(state, limit=21)) is not None:
            winning_states[winner] += universes
            continue

        for roll, roll_universes in ROLLS.items():
            new_state = mutate(state, roll)
            states[new_state] = states.get(new_state, 0) + (universes * roll_universes)
    return max(winning_states)


if __name__ == '__main__':
    # It's convenient to have the player locs be 0-9 instead of 1-10 so modulo works
    player_locs = [int(x[-2:].strip())-1 for x in read_data().splitlines()]
    print(f"Part one: {part_one(player_locs)}")
    print(f"Part two: {part_two(player_locs)}")

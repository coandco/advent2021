from utils import read_data
from typing import Generator, List, Tuple, Dict, Optional


def fixed_die(start: int = 1, sides: int = 100) -> Generator[int, None, None]:
    while True:
        yield from range(start, sides+1)


def part_one(player_locs: List[int]) -> int:
    player_locs = player_locs[:]
    player_scores = [0] * len(player_locs)
    die = fixed_die()
    num_rolls = 0
    done = False
    while True:
        for i in range(len(player_locs)):
            rolls = (next(die), next(die), next(die))
            player_locs[i] = (player_locs[i] + sum(rolls)) % 10
            player_scores[i] += player_locs[i] + 1  # +1 because 1-10 instead of 0-9
            num_rolls += 3
            if player_scores[i] >= 1000:
                done = True
                break
        if done:
            break
    return min(player_scores) * num_rolls


WorldState = Tuple[Tuple[int, int], Tuple[int, int], int]


# roll distribution for three rolls
ROLLS = {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}


def mutate_part_two(state: WorldState, roll: int) -> WorldState:
    locs, scores, pnum = state

    new_loc = (locs[pnum] + roll) % 10
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


def part_two(starting_locs: List[int]) -> int:
    states: Dict[WorldState, int] = {((starting_locs[0], starting_locs[1]), (0, 0), 0): 1}
    winning_states: List[int] = [0, 0]

    while states:
        # Python dicts are ordered since 3.5, and this will get the first-inserted item from the list and delete it
        state, universes = next(iter(states.items()))
        del states[state]

        if (winner := state_winner(state)) is not None:
            winning_states[winner] += universes
            continue

        for roll, roll_universes in ROLLS.items():
            new_state = mutate_part_two(state, roll)
            states[new_state] = states.get(new_state, 0) + (universes * roll_universes)
    return max(winning_states)


if __name__ == '__main__':
    player_locs = [int(x[-1])-1 for x in read_data().splitlines()]
    print(f"Part one: {part_one(player_locs)}")
    print(f"Part two: {part_two(player_locs)}")

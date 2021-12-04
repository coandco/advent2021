from utils import read_data
from typing import List, Tuple
import numpy as np


def read_bingo_board(boardstr: str) -> np.ndarray:
    board = np.zeros((5, 5), dtype=int)
    for i, line in enumerate(boardstr.splitlines()):
        for j, numstr in enumerate(line.split()):
            board[i, j] = int(numstr)
    return board


def mark_boards(boards: List[np.ndarray], markings: List[np.ndarray], to_mark: int) -> List[np.ndarray]:
    for i, board in enumerate(boards):
        for idx, value in np.ndenumerate(board):
            if value == to_mark:
                markings[i][idx] = True
    return markings


def check_board(board_marking: np.ndarray) -> bool:
    # Check each row
    for i in range(board_marking.shape[0]):
        slice = board_marking[i, :]
        if np.all(slice):
            return True
    for i in range(board_marking.shape[1]):
        if np.all(board_marking[:, i]):
            return True
    return False


def find_completed_board(boards: List[np.ndarray], markings: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray] | None:
    for i, marking in enumerate(markings):
        if check_board(marking):
            return boards[i], markings[i]
    return None


def move_completed_boards(boards: List[np.ndarray], markings: List[np.ndarray]) -> Tuple[List[np.ndarray], List[np.ndarray], List[np.ndarray], List[np.ndarray]]:
    active_boards = []
    active_markings = []
    completed_boards = []
    completed_markings = []
    for i, marking in enumerate(markings):
        if check_board(marking):
            completed_boards.append(boards[i])
            completed_markings.append(markings[i])
        else:
            active_boards.append(boards[i])
            active_markings.append(markings[i])
    return active_boards, active_markings, completed_boards, completed_markings


def score_board(board: np.ndarray, marking: np.ndarray) -> int:
    score = 0
    for idx, value in np.ndenumerate(marking):
        if not value:
            score += board[idx]
    return score


def run_bingo(called_numbers: List[int], boards: List[np.ndarray]) -> Tuple[int, int]:
    markings = [np.zeros((5, 5), dtype=bool) for x in range(len(INPUT[1:]))]
    completed_boards = []
    completed_markings = []
    part_one_score = 0
    part_one_number = 0
    for number in called_numbers:
        markings = mark_boards(boards, markings, number)
        boards, markings, newly_completed_boards, newly_completed_markings = move_completed_boards(boards, markings)
        # If we're adding our first completed board to the list, note it down
        if len(completed_boards) == 0 and len(newly_completed_boards) > 0:
            part_one_score = score_board(newly_completed_boards[0], newly_completed_markings[0])
            part_one_number = number
        completed_boards.extend(newly_completed_boards)
        completed_markings.extend(newly_completed_markings)
        if len(boards) == 0:
            part_two_score = score_board(completed_boards[-1], completed_markings[-1])
            return part_one_score * part_one_number, part_two_score * number


if __name__ == '__main__':
    INPUT = read_data().split("\n\n")
    called_numbers = [int(x) for x in INPUT[0].split(",")]
    boards = [read_bingo_board(x) for x in INPUT[1:]]
    part_one, part_two = run_bingo(called_numbers, boards)
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")




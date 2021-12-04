from utils import read_data
from typing import List, Tuple
import numpy as np


def read_bingo_board(boardstr: str) -> np.ndarray:
    board = np.zeros((5, 5), dtype=int)
    for i, line in enumerate(boardstr.splitlines()):
        for j, numstr in enumerate(line.split()):
            board[i, j] = int(numstr)
    return board


def mark_boards(boards: List[np.ndarray], to_mark: int) -> List[np.ndarray]:
    for i, board in enumerate(boards):
        board[board == to_mark] = -1
    return boards


def check_board(board: np.ndarray) -> bool:
    # Check each row
    marked_locations = board == -1
    for i in range(marked_locations.shape[0]):
        slice = marked_locations[i, :]
        if np.all(slice):
            return True
    # Check each column
    for i in range(marked_locations.shape[1]):
        if np.all(marked_locations[:, i]):
            return True
    return False


def move_completed_boards(boards: List[np.ndarray]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    active_boards = []
    completed_boards = []
    for board in boards:
        if check_board(board):
            completed_boards.append(board)
        else:
            active_boards.append(board)
    return active_boards, completed_boards


def score_board(board: np.ndarray) -> int:
    return board[board != -1].sum()


def run_bingo(called_numbers: List[int], boards: List[np.ndarray]) -> Tuple[int, int]:
    completed_boards = []
    part_one_score = 0
    part_one_number = 0
    for number in called_numbers:
        boards = mark_boards(boards, number)
        boards, newly_completed_boards = move_completed_boards(boards)
        # If we're adding our first completed board to the list, note it down
        if len(completed_boards) == 0 and len(newly_completed_boards) > 0:
            part_one_score = score_board(newly_completed_boards[0])
            part_one_number = number
        completed_boards.extend(newly_completed_boards)
        if len(boards) == 0:
            part_two_score = score_board(completed_boards[-1])
            return part_one_score * part_one_number, part_two_score * number


if __name__ == '__main__':
    INPUT = read_data().split("\n\n")
    called_numbers = [int(x) for x in INPUT[0].split(",")]
    boards = [read_bingo_board(x) for x in INPUT[1:]]
    part_one, part_two = run_bingo(called_numbers, boards)
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")




from collections import Counter
from typing import List, Tuple

import numpy as np


def read_data(raw_data_file: str) -> Tuple[List[int], List[List[List[int]]]]:
    """
    Reads input data and splits the called numbers from the bingo board data
    """
    with open(raw_data_file, "r") as f:
        called_numbers = list(map(int, f.readline().rstrip().split(",")))
        next(f)
        raw_grids = f.read().split("\n\n")
    boards = []
    for raw_grid in raw_grids:
        rows = raw_grid.split("\n")
        boards.append(np.array([list(map(int, row.split())) for row in rows]))
    return called_numbers, boards


class Game:
    """
    Main class governing the playing of the bingo game across multiple `boards`
    as numbers are called sequentially from `called_numbers`
    """

    def __init__(self, called_numbers: List[int], boards: List[List[List[int]]]):
        self.called_numbers = called_numbers
        self.boards = [BingoBoard(board) for board in boards]

    def get_board_scores(self) -> int:
        """
        Returns scores for all boards over the entirety of the game; scores are
        logged as each board wins (i.e., order of winning boards is preserved)
        """
        remaining_boards = self.boards.copy()
        winning_boards = []
        for called_number in called_numbers:
            for board in remaining_boards:
                board.play_round(called_number)
                if board.get_win_status():
                    winning_boards.append((board, called_number))
            remaining_boards = [
                board
                for board in remaining_boards
                if board not in [board for board, _ in winning_boards]
            ]
        return [
            winning_board.get_sum_of_unmatched_numbers() * winning_called_number
            for winning_board, winning_called_number in winning_boards
        ]


class BingoBoard:
    """
    Class modeling behavior of a single Bingo board
    """

    def __init__(self, board_array: np.array):
        self.board = board_array
        self.matched_numbers_indices = set()

    def _get_indices_of_called_number(
        self, called_number: int
    ) -> List[Tuple[int, int]]:
        """
        Returns the indices of a matched number or returns an empty list if the
        `called_number` is not found on the board
        """
        return list(zip(*np.where(self.board == called_number)))

    def play_round(self, called_number: int):
        """
        Simulates one round of bingo by keeping track of the indices of any
        matched numbers (numbers on the board that match the `called_number`)
        """
        matched_indices = self._get_indices_of_called_number(called_number)
        if matched_indices:
            for idx in matched_indices:
                self.matched_numbers_indices.add(idx)

    def get_win_status(self) -> bool:
        """
        Evaluates board and returns boolean value corresponding to whether the
        board has won yet (based on the last round played)
        """
        if len(self.matched_numbers_indices) < 5:
            return False
        row_matches, col_matches = tuple(
            Counter(direction) for direction in zip(*self.matched_numbers_indices)
        )
        return (
            row_matches.most_common(1)[0][1] == self.board.shape[0]
            or col_matches.most_common(1)[0][1] == self.board.shape[1]
        )

    def get_sum_of_unmatched_numbers(self) -> int:
        """
        Returns the sum of the numbers on the board that have not been called
        """
        sum_array = np.copy(self.board)
        matched_numbers_indices_array = np.array(list(self.matched_numbers_indices))
        sum_array[
            matched_numbers_indices_array[:, 0], matched_numbers_indices_array[:, 1]
        ] = 0
        return sum_array.sum().sum()


if __name__ == "__main__":
    called_numbers, boards = read_data("./bingo_rd.txt")
    game = Game(called_numbers, boards)
    scores = game.get_board_scores()
    print(scores[0])  # Part 1 Solution: 11536
    print(scores[-1])  # Part 2 Solution: 1284

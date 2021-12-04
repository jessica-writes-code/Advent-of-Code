from dataclasses import dataclass
import itertools
from typing import List

import numpy as np


BOARD_SIZE = 5


@dataclass
class Board:
    """Represents a Bingo board"""

    contents: np.array
    marked_contents: np.array

    def mark_called_number(self, num: int):
        matches = self.contents == num
        self.marked_contents = self.marked_contents + matches

    def is_winner(self) -> bool:
        is_winner_col = max(np.sum(self.marked_contents, axis=0)) == BOARD_SIZE
        is_winner_row = max(np.sum(self.marked_contents, axis=1)) == BOARD_SIZE
        return is_winner_col or is_winner_row

    def score(self, last_num: int) -> int:
        return np.sum(np.invert(self.marked_contents) * self.contents) * last_num


# Load info
with open("./Day4Input.txt") as f:
    input = [x.strip() for x in f.readlines()]

# Collect info into data structures
numbers_called = [int(x) for x in input[0].split(",")]

boards = []
for i in range(2, len(input) - 1, BOARD_SIZE + 1):
    board_content = input[i : i + BOARD_SIZE]
    board_content_parsed = [[int(x) for x in row.split()] for row in board_content]
    boards.append(
        Board(
            contents=np.array(board_content_parsed),
            marked_contents=np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=bool),
        )
    )

# Play game until there's a winner
for num in numbers_called:
    for i in range(len(boards)):
        boards[i].mark_called_number(num)
        if boards[i].is_winner():
            print(boards[i].score(num))
            exit()

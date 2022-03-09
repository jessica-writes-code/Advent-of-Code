from typing import Tuple

import numpy as np

from _base import Solver


class Day5Solver(Solver):

    NUM_ROWS = 128
    NUM_COLUMNS = 8

    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.input = [line for line in self.raw_input]

    def _get_seat_element(self, seat_str_part: str, is_row: bool = True) -> int:
        """Find the row or column id (as an integer) from the boarding pass string"""
        el_min = 0
        el_max = self.NUM_ROWS - 1 if is_row else self.NUM_COLUMNS - 1
        for entry in seat_str_part:
            if entry in ['F', 'L']:
                el_max = el_max - (el_max - el_min + 1) / 2
            elif entry in ['B', 'R']:
                el_min = el_min + (el_max - el_min + 1) / 2
        assert el_min == el_max
        return int(el_min)

    def _get_seat_info(self, seat_str: str) -> Tuple[int, int]:
        """Find the row and column indicated by the boarding pass string"""
        return (
            self._get_seat_element(seat_str[0:7]),
            self._get_seat_element(seat_str[7:], False),
        )

    def _get_seat_id(self, row_num: int, col_num: int) -> int:
        """Find the 'Seat ID', based on the Row & Column of the seat"""
        return row_num * 8 + col_num

    def solve_part1(self) -> int:
        """Find the highest 'Seat ID' on any boarding pass"""
        seat_ids = [
            self._get_seat_id(*self._get_seat_info(seat_str)) for seat_str in self.input
        ]
        return max(seat_ids)

    def solve_part2(self) -> int:
        """Find my seat, which will be the only empty seat not at the front or
        back of the plane"""
        seat_tracker = np.zeros((self.NUM_ROWS, self.NUM_COLUMNS))
        seat_ids = [self._get_seat_info(seat_str) for seat_str in self.input]
        for seat_id in seat_ids:
            seat_tracker[seat_id[0]][seat_id[1]] = 1
        empty_seats = np.where(seat_tracker == 0)
        return [
            self._get_seat_id(x, y)
            for x, y in zip(empty_seats[0], empty_seats[1])
            if 1 < x < 102
        ][0]


solver = Day5Solver("./input/Day5Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

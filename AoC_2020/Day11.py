from typing import Callable

import numpy as np

from _base import Solver


class Day11Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.input = np.array([list(x) for x in self.raw_input])

    def _find_final_seats_occupied(
        self,
        number_occupied_fn: Callable[[int, int, np.ndarray], int],
        max_occupied: int,
    ) -> int:
        """Find the number of occupied seats, once the process of taking/abandoning
        seats has reached stability. The process is such that:
            (1) if an empty seat has no occupied, adjacent seats, it becomes occupied
            (2) if an occupied seat has too many occupied, adjacent seats, it becomes
                empty
        The definition of adjacent varies and is specified by the `number_occupied_fn`.

        Args:
            number_occupied_fn: Callable[[int, int, np.ndarray], int] - function to
                determine the number of occupied seats adjacent to a particular seat,
                given a particular layout
            max_occupied: int - maximum number of adjacent, occupied seats that an
                individual person will find acceptable

        Returns:
            int - number of occupied seats, once the layout stops changing
        """
        layout, new_layout = self.input.copy(), None

        while not (layout == new_layout).all():
            if new_layout is not None:
                layout = (
                    new_layout.copy()
                )  # Layout is the "New Layout" from the last iteration
            new_layout = layout.copy()

            for iy, ix in np.ndindex(layout.shape):
                current_seat_status = layout[iy, ix]
                if current_seat_status == ".":
                    continue
                number_occupied = number_occupied_fn(iy, ix, layout)

                # Rule 1: If a seat is empty (L) and there are no occupied seats adjacent to it,
                # the seat becomes occupied.
                if current_seat_status == "L" and number_occupied == 0:
                    new_layout[iy, ix] = "#"

                # Rule 2: If a seat is occupied (#) and `max_occupied` or more seats adjacent to
                # it are also occupied, the seat becomes empty.
                if current_seat_status == "#" and number_occupied >= max_occupied:
                    new_layout[iy, ix] = "L"

        return np.sum(layout == "#")

    def solve_part1(self) -> int:
        def num_adjacent_fn1(y: int, x: int, current_layout: np.ndarray) -> int:
            """Determine the number of occupied seats immediately next to a seat of
            interest, where 'next to' can be above, below, left, right, or diagonal
            
            Args:
                y: int - y value of seat of interest
                x: int - x value of seat of interest
                current_layout: np.ndarray - current layout of seats

            Returns:
                int - number of occupied seats immediately next to seat of interest
            """
            # Get the patch of seats surrounding the seat of interest,
            # where the seat of interest is marked with a 'C'
            current_layout = current_layout.copy()
            current_layout[y][x] = "C"

            min_y, max_y = max(0, y - 1), min(current_layout.shape[0] - 1, y + 1)
            min_x, max_x = max(0, x - 1), min(current_layout.shape[1] - 1, x + 1)
            patch = current_layout[min_y : max_y + 1, min_x : max_x + 1].copy()

            # Count occupied seats in patch (not including seat of interest)
            return np.sum(patch == "#")

        return self._find_final_seats_occupied(num_adjacent_fn1, 4)

    def solve_part2(self) -> int:
        def _occupied_first(line_of_sight: np.ndarray) -> bool:
            for entry in line_of_sight:
                if entry != ".":
                    return entry == "#"
            return False

        def num_adjacent_fn2(y: int, x: int, current_layout: np.ndarray) -> int:
            """Determine the number of occupied seats that can be seen (in any direction)
            from a seat of interest. Occupied seats cannot be seen 'through' empty seats.
            
            Args:
                y: int - y value of seat of interest
                x: int - x value of seat of interest
                current_layout: np.ndarray - current layout of seats

            Returns:
                int - the number of occupied seats that can be seen from a seat of interest
            """
            count = 0

            # Vertical & Horizontal
            vertical, horizontal = current_layout[:, x], current_layout[y, :]
            count += _occupied_first(np.flip(vertical[0:y]))  # Above
            count += _occupied_first(vertical[y + 1 :])  # Below
            count += _occupied_first(np.flip(horizontal[0:x]))  # Left
            count += _occupied_first(horizontal[x + 1 :])  # Right

            # Diagonals
            count += _occupied_first(
                np.flip(current_layout[0:y, 0:x]).diagonal()
            )  # Upper left
            count += _occupied_first(
                np.flipud(current_layout[0:y, x + 1 :]).diagonal()
            )  # Upper right
            count += _occupied_first(
                np.fliplr(current_layout[y + 1 :, 0:x]).diagonal()
            )  # Lower left
            count += _occupied_first(
                current_layout[y + 1 :, x + 1 :].diagonal()
            )  # Lower right

            return count

        return self._find_final_seats_occupied(num_adjacent_fn2, 5)


solver = Day11Solver("./input/Day11Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

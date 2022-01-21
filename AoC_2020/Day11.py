from xxlimited import new
import numpy as np

from _base import Solver


class Day11Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.input = np.array([list(x) for x in self.raw_input])

    def solve_part1(self) -> int:
        """TODO"""
        layout, new_layout = self.input.copy(), None

        while True:  # TODO : Definitely not this
            new_layout = layout.copy()

            for iy, ix in np.ndindex(layout.shape):
                min_y, max_y = max(0, iy - 1), min(layout.shape[0] - 1, iy + 1)
                min_x, max_x = max(0, ix - 1), min(layout.shape[1] - 1, ix + 1)

                # TODO: This can probably be reduced
                current_seat_status = layout[iy, ix]
                temp_layout = layout.copy()
                temp_layout[iy][ix] = 'C'
                patch = temp_layout[min_y:max_y+1, min_x:max_x+1]
                num_adjacent_occupied_seats = np.sum(patch == '#')

                # If a seat is empty (L) and there are no occupied seats adjacent to it,
                # the seat becomes occupied.
                if current_seat_status == 'L' and num_adjacent_occupied_seats == 0:
                    new_layout[iy, ix] = '#'

                # If a seat is occupied (#) and four or more seats adjacent to it are also
                # occupied, the seat becomes empty.
                if current_seat_status == '#' and num_adjacent_occupied_seats >= 4:
                    new_layout[iy, ix] = 'L'
        
            if (layout == new_layout).all():
                break
            layout = new_layout.copy()

        return np.sum(layout == '#')
            

    def solve_part2(self) -> int:
        """TODO"""
        import pdb
        pdb.set_trace()


solver = Day11Solver("./input/Day11Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

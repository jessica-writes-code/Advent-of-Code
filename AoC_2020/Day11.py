from xxlimited import new
import numpy as np

from _base import Solver


class Day11Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.input = np.array([list(x) for x in self.raw_input])

    def solve_part1(self) -> int:
        """TODO: Documentation / comments"""
        layout, new_layout = self.input.copy(), None

        while not (layout == new_layout).all():
            if new_layout is not None:
                layout = new_layout.copy()
            new_layout = layout.copy()

            for iy, ix in np.ndindex(layout.shape):
                min_y, max_y = max(0, iy - 1), min(layout.shape[0] - 1, iy + 1)
                min_x, max_x = max(0, ix - 1), min(layout.shape[1] - 1, ix + 1)

                current_seat_status = layout[iy, ix]
                
                layout[iy][ix] = 'C'
                patch = layout[min_y:max_y+1, min_x:max_x+1].copy()
                layout[iy][ix] = current_seat_status
                
                num_adjacent_occupied_seats = np.sum(patch == '#')

                # If a seat is empty (L) and there are no occupied seats adjacent to it,
                # the seat becomes occupied.
                if current_seat_status == 'L' and num_adjacent_occupied_seats == 0:
                    new_layout[iy, ix] = '#'

                # If a seat is occupied (#) and four or more seats adjacent to it are also
                # occupied, the seat becomes empty.
                if current_seat_status == '#' and num_adjacent_occupied_seats >= 4:
                    new_layout[iy, ix] = 'L'

        return np.sum(layout == '#')
            

    def solve_part2(self) -> int:
        """TODO"""
        import pdb
        pdb.set_trace()


solver = Day11Solver("./input/Day11Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

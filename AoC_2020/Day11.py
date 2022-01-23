from xxlimited import new
import numpy as np

from _base import Solver


class Day11Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.input = np.array([list(x) for x in self.raw_input])

    def _find_final_seats_occupied():
        pass  # TODO: Use this to generalize code

    def solve_part1(self) -> int:
        """Find the number of seats that are occupied once the process of seat
        movement reaches stability"""
        layout, new_layout = self.input.copy(), None

        while not (layout == new_layout).all():
            if new_layout is not None:
                layout = new_layout.copy()  # Layout is the "New Layout" from the last iteration
            new_layout = layout.copy()

            for iy, ix in np.ndindex(layout.shape):
                current_seat_status = layout[iy, ix]
                
                # Get the patch of seats surrounding the seat of interest,
                # where the seat of interest is marked with a 'C'
                min_y, max_y = max(0, iy - 1), min(layout.shape[0] - 1, iy + 1)
                min_x, max_x = max(0, ix - 1), min(layout.shape[1] - 1, ix + 1)
                layout[iy][ix] = 'C'
                patch = layout[min_y:max_y+1, min_x:max_x+1].copy()
                layout[iy][ix] = current_seat_status
                
                num_adjacent_occupied_seats = np.sum(patch == '#')

                # Rule 1: If a seat is empty (L) and there are no occupied seats adjacent to it,
                # the seat becomes occupied.
                if current_seat_status == 'L' and num_adjacent_occupied_seats == 0:
                    new_layout[iy, ix] = '#'

                # Rule 2: If a seat is occupied (#) and four or more seats adjacent to it are also
                # occupied, the seat becomes empty.
                if current_seat_status == '#' and num_adjacent_occupied_seats >= 4:
                    new_layout[iy, ix] = 'L'

        return np.sum(layout == '#')
            

    def solve_part2(self) -> int:
        """TODO"""
        layout, new_layout = self.input.copy(), None

        while not (layout == new_layout).all():
            if new_layout is not None:
                layout = new_layout.copy()  # Layout is the "New Layout" from the last iteration
            new_layout = layout.copy()

            for iy, ix in np.ndindex(layout.shape):
                current_seat_status = layout[iy, ix]
                if current_seat_status == '.':
                    continue  # Don't bother evaluating the floor
                
                # Find number of occupied seats that can be seen
                # TODO: First seat seen! Not any seat...
                num_adjacent_occupied_seats = sum(
                    [
                        (layout[iy][0:ix] == '#').any(),  # Left
                        (layout[iy][ix+1:] == '#').any(),  # Right
                        (layout[0:iy][:,ix] == '#').any(),  # Above
                        (layout[iy+1:][:,ix] == '#').any(),  # Below
                        (np.flip(layout[0:iy][:,0:ix]).diagonal() == '#').any(),  # Upper-left diagonal
                        (np.rot90(layout[0:iy][:,ix+1:], k=3).diagonal() == '#').any(),  # Upper-right diagonal
                        (np.rot90(layout[iy+1:][:,0:ix]).diagonal() == '#').any(),  # Lower-left diagonal
                        (layout[iy+1:][:,ix+1:].diagonal() == '#').any(),  # Lower-right diagonal
                    ]
                )
                
                # Rule 1: If a seat is empty (L) and there are no occupied seats adjacent to it,
                # the seat becomes occupied.
                if current_seat_status == 'L' and num_adjacent_occupied_seats == 0:
                    new_layout[iy, ix] = '#'

                # Rule 2: TODO
                if current_seat_status == '#' and num_adjacent_occupied_seats >= 5:
                    new_layout[iy, ix] = 'L'

            import pdb
            pdb.set_trace()

        return np.sum(layout == '#')


solver = Day11Solver("./input/Day11Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

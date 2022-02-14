from functools import reduce
import itertools

from _base import Solver


class Day1Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.input = [int(line) for line in self.raw_input]

    def solve(self, n):
        """Find `n` numbers in the input whose sum is 2020
        and return their product"""
        for nums in itertools.combinations(self.input, n):
            if sum(nums) == 2020:
                return reduce(lambda x, y: x*y, nums)

    def solve_part1(self) -> int:
        """Solve for `n` = 2"""
        return self.solve(2)

    def solve_part2(self) -> int:
        """Solve for `n` = 3"""
        return self.solve(3)


solver = Day1Solver("./input/Day1Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

# Problem: https://adventofcode.com/2019/day/2

from re import I
from typing import List


class Day2Solver():
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        with open(file_path) as f:
            self.raw_input = [x.strip() for x in f.readlines()]
        self.input = [int(x) for x in self.raw_input[0].split(',')]

    @staticmethod
    def execute_instructions(values: List[int]) -> int:
        position = 0
        while position <= len(values):

            if values[position] in (1, 2):
                idx1 = values[position + 1]
                idx2 = values[position + 2]
                idx3 = values[position + 3]

                val1 = values[idx1]
                val2 = values[idx2]

                if values[position] == 1:
                    values[idx3] = val1 + val2
                elif values[position] == 2:
                    values[idx3] = val1 * val2

                position += 4
            
            elif values[position] == 99:
                break

            else:
                raise ValueError('Something has gone horribly wrong!')
        
        return values[0]


    def solve_part1(self) -> int:
        values = self.input.copy()
        values[1] = 12
        values[2] = 2
        return self.execute_instructions(values)


    def solve_part2(self, target_output: int = 19690720) -> int:
        for i in range(100):
            for j in range(100):
                values = self.input.copy()
                values[1] = i
                values[2] = j
                if self.execute_instructions(values) == target_output:
                    return 100 * i + j
        return None


if __name__ == "__main__":
    solver = Day2Solver("Day2Input.txt")
    print('The solution to part 1 is', solver.solve_part1())
    print('The solution to part 2 is', solver.solve_part2())

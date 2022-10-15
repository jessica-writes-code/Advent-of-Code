# Problem: https://adventofcode.com/2019/day/4

from typing import List, Optional


class Day4Solver:
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        with open(file_path) as f:
            self.raw_input = [x.strip() for x in f.readlines()]
        self.input = [int(x) for x in self.raw_input[0].split('-')]

    @staticmethod
    def has_n_adjacent_digits(number: int, n_digits: Optional[int] = None):
        """Determines whether a number has exactly N adjacent digits that are
        the same. If no value `n_digits` is provided, determines whether a number
        has any adjacent digits that are the same."""
        str_number = str(number)
        num_parts = []

        for i in str_number:
            if len(num_parts) == 0:
                num_parts.append(i)
            elif num_parts[-1][-1] == i:
                num_parts[-1] += i
            else:
                num_parts.append(i)
        
        num_part_lengths = [len(x) for x in num_parts]
        
        if n_digits:
            return any([x == n_digits for x in num_part_lengths])
        else:
            return any([x > 1 for x in num_part_lengths])

    @staticmethod
    def has_nondecreasing_digits(number: int):
        """Determines whether a number has nondecreasing consecutive digits."""
        str_number = str(number)
        for i in range(0, len(str_number)-1):
            if str_number[i] > str_number[i+1]:
                return False
        return True

    def count_passwords(self, start: int, stop: int, n_digits: Optional[int] = None) -> int:
        """Counts passwords in a given range that meet specified requirements."""
        counter = 0
        for i in range(start, stop + 1):
            if not self.has_n_adjacent_digits(i, n_digits):
                continue
            
            if not self.has_nondecreasing_digits(i):
                continue

            counter += 1

        return counter

    def solve_part1(self) -> int:
        """Solves Part 1."""
        return self.count_passwords(self.input[0], self.input[1])

    def solve_part2(self) -> int:
        """Solves Part 2."""
        return self.count_passwords(self.input[0], self.input[1], 2)


if __name__ == "__main__":
    solver = Day4Solver("Day4Input.txt")
    print('The solution to part 1 is', solver.solve_part1())
    print('The solution to part 2 is', solver.solve_part2())

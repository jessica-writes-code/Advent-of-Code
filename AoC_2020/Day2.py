from collections import Counter
from dataclasses import dataclass

from _base import Solver


@dataclass
class InputLine:
    """Represents a single line of the puzzle input, a policy (composed
    of two numbers, and a letter) and a password that the policy applies to"""

    letter: str
    num1: int
    num2: int
    password: str

    def password_meets_policy1(self) -> bool:
        """Determines whether the password meets the policy of the sled
        rental place down the street"""
        counter = Counter(self.password)
        return self.num1 <= counter[self.letter] <= self.num2

    def password_meets_policy2(self) -> bool:
        """Determines whether the password meets the policy of the Official
        Toboggan Corporate Authentication System"""
        return (self.password[self.num1 - 1] == self.letter) ^ (
            self.password[self.num2 - 1] == self.letter
        )


class Day2Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.input = []
        for line in self.raw_input:
            split_line = line.split(" ")
            num1, num2 = split_line[0].split("-")
            letter = split_line[1].replace(":", "")
            password = split_line[2]
            self.input.append(InputLine(letter, int(num1), int(num2), password))

    def solve_part1(self) -> int:
        """Counts the number of passwords meeting the policy of the sled
        rental place down the street"""
        return sum([x.password_meets_policy1() for x in self.input])

    def solve_part2(self) -> int:
        """Counts the number of passwords meeting the policy of the Official
        Toboggan Corporate Authentication System"""
        return sum([x.password_meets_policy2() for x in self.input])


solver = Day2Solver("./input/Day2Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

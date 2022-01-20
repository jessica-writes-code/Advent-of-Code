from collections import Counter
from typing import List

from _base import Solver


class Day6Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.groups: List[List[str]] = []
        group = []
        for el in self.raw_input:
            if el != "":
                group.append(el)
            else:
                self.groups.append(group)
                group = []
        self.groups.append(group)

    def solve_part1(self) -> int:
        """Find the number of distinct quesitons to which at least one group member
        answered yes; sum these numbers across groups"""
        return sum([len(Counter("".join(group))) for group in self.groups])

    def solve_part2(self) -> int:
        """Find the number of questions to which everyone in the group answered yes;
        sum these numbers across groups"""
        return sum(
            [
                len([v for _, v in Counter("".join(group)).items() if v == len(group)])
                for group in self.groups
            ]
        )


solver = Day6Solver("./input/Day6Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

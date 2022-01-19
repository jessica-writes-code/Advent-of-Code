from abc import ABC, abstractmethod

class Solver(ABC):
    """Abstract base class for Advent of Code puzzle-solver"""

    def __init__(self, file_path: str):
        """Load input"""
        with open(file_path) as f:
            self.raw_input = [x.strip() for x in f.readlines()]

    @abstractmethod
    def solve_part1(self) -> int:
        """Solve part 1"""

    @abstractmethod
    def solve_part2(self) -> int:
        """Solve part 2"""

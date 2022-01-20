from collections import defaultdict
from typing import Dict

from _base import Solver


MY_BAG_TYPE = "shiny gold bag"


class Day7Solver(Solver):
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        super().__init__(file_path)
        self.rules_dict = {}
        for line in self.raw_input:
            outer, inner = line.split(" contain ")
            inner_bags = inner.replace(".", "").split(", ")

            inner_bag_info = []
            for bag in inner_bags:
                if bag == "no other bags":
                    info = (0, None)
                else:
                    bag_split = bag.split()
                    num, bag_type = int(bag_split[0]), " ".join(bag_split[1:])
                    info = (num, bag_type.replace("bags", "bag"))
                inner_bag_info.append(info)

            self.rules_dict[outer.replace("bags", "bag")] = inner_bag_info

    def _bag_contents(self, bag: str) -> Dict[str, int]:
        """Find all contents of a given bag
        
        Returns:
            Dict[str, int] in which keys are bag types and values are the number
                of bags of that type
        """
        bag_contents = defaultdict(int)
        for num, bag_type in self.rules_dict[bag]:
            if bag_type is not None:
                bag_contents[bag_type] += num
                inner_bag_contents = self._bag_contents(bag_type)
                bag_contents = self._add_inner_bags(
                    bag_contents, inner_bag_contents, num
                )
        return bag_contents

    @staticmethod
    def _add_inner_bags(
        bag_contents: Dict[str, int],
        inner_bag_contents: Dict[str, int],
        number_of_inner_bags: int,
    ):
        """Add a inner bag contents to the current contents of a bag"""
        for bag_type, number_of_bags in inner_bag_contents.items():
            bag_contents[bag_type] += number_of_bags * number_of_inner_bags
        return bag_contents

    def solve_part1(self) -> int:
        """Determine the number of types of bags that can eventually contain
        at least one shiny gold bag"""
        return sum(
            [MY_BAG_TYPE in self._bag_contents(k) for k, _ in self.rules_dict.items()]
        )

    def solve_part2(self) -> int:
        """Determine the total number of bags that are contained within one
        shiny gold bag"""
        return sum([v for _, v in self._bag_contents(MY_BAG_TYPE).items()])


solver = Day7Solver("./input/Day7Input.txt")
print(solver.solve_part1())
print(solver.solve_part2())

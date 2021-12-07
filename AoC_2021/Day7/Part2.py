from collections import Counter
from typing import List


def find_cost(position: int, positions_dict: List[int]):
    total_cost = 0
    for k, v in positions_dict.items():
        total_cost += sum([i for i in range(1, abs(k - position) + 1)]) * v
    return total_cost


def get_cheapest_position(positions_dict: List[int]):
    max_position = max(positions_dict.keys())
    min_cost, min_cost_position = float('inf'), None
    for i in range(max_position):
        cost = find_cost(i, positions_dict)
        if cost < min_cost:
            min_cost, min_cost_position = cost, i
    return min_cost, min_cost_position


with open("./Day7Input.txt") as f:
    positions = [int(x) for x in f.read().split(",")]
positions_dict = Counter(positions)


print(get_cheapest_position(positions_dict))

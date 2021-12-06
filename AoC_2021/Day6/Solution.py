from collections import Counter, defaultdict
from typing import Dict


def simulate(state_dict: Dict[int, int], num_days: int):
    for _ in range(num_days):
        new_state_dict = defaultdict(int)
        for days_remaining, fish_count in state_dict.items():
            if days_remaining == 0:
                new_state_dict[6] += fish_count
                new_state_dict[8] += fish_count
            else:
                new_state_dict[days_remaining - 1] += fish_count
        state_dict = new_state_dict
    return state_dict


with open("./Day6Input.txt") as f:
    state = [int(x) for x in f.read().split(",")]
state_dict = Counter(state)

print(sum(simulate(state_dict, 80).values()))
print(sum(simulate(state_dict, 256).values()))

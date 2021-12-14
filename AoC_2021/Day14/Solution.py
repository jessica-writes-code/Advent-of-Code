from collections import defaultdict
from typing import Dict, List, Tuple

def parse_puzzle_input(puzzle_input: List[str]) -> Tuple[str, Dict[str, str]]:
    template = puzzle_input[0]
    
    rules = {}
    for i in range(2, len(puzzle_input)):
        k, v = puzzle_input[i].split(' -> ')
        rules[k] = v

    return template, rules


def pairs_from_template(x: str) -> Dict[str, int]:
    d = defaultdict(int)
    for i in range(0, len(x) - 1):
        d[x[i:i+2]] += 1
    return dict(d)


def run_step(count_dict: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    new_count_dict = defaultdict(int)
    for k, v in count_dict.items():
        first_pair = k[0] + rules[k]
        new_count_dict[first_pair] += v
        second_pair = rules[k] + k[1]
        new_count_dict[second_pair] += v      
    return dict(new_count_dict)


def letter_count_from_pair_count(pair_count: Dict[str, int], template: str) -> Dict[str, int]:
    letter_count_dict = defaultdict(int)
    for k, v in pair_count.items():
        letter_count_dict[k[0]] += v
        letter_count_dict[k[1]] += v
    letter_count_dict[template[0]] += 1
    letter_count_dict[template[-1]] += 1

    for k, v in letter_count_dict.items():
        letter_count_dict[k] = v // 2

    return dict(letter_count_dict)


def solve(template: str, rules: Dict[str, str], steps: int) -> int:
    pair_count_dict = pairs_from_template(template)
    for _ in range(steps):
        pair_count_dict = run_step(pair_count_dict, rules)
    letter_count_dict = letter_count_from_pair_count(pair_count_dict, template)
    counts = letter_count_dict.values()
    return max(counts) - min(counts)


with open("./Day14Input.txt") as f:
    puzzle_input = [x.strip() for x in f.readlines()]
template, rules = parse_puzzle_input(puzzle_input)

print(solve(template, rules, 10))
print(solve(template, rules, 40))

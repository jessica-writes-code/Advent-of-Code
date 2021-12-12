from collections import Counter

from typing import List, Set


# Part 1
def is_small_cave(identifier: str):
    return not (identifier in ["start", "end"]) and identifier.lower() == identifier


def find_possible_next_locations(
    puzzle_input: List[Set[str]], current_path: List[str], part2=False
) -> List[str]:
    current_location = current_path[-1]

    # If you're at the end, there's nowhere to go!
    if current_location == "end":
        return []

    # Find places you could go next
    possible_next_locations = [
        rt - {current_location} for rt in puzzle_input if current_location in rt
    ]
    assert sum([len(x) == 1 for x in possible_next_locations]) == len(
        possible_next_locations
    )
    possible_next_locations = [x.pop() for x in possible_next_locations]
    possible_next_locations = [x for x in possible_next_locations if x != "start"]

    # Check that those places are valid vis-a-vis the small cave constraint
    if not part2:
        possible_next_locations = [
            loc
            for loc in possible_next_locations
            if not is_small_cave(loc) or loc not in current_path
        ]
    else:
        possible_next_locations = [
            loc
            for loc in possible_next_locations
            if not is_small_cave(loc) or can_go_small_cave(loc, current_path)
        ]

    return possible_next_locations


def extend_path(puzzle_input: List[Set[str]], current_path: List[str], part2=False) -> List[str]:

    # If you're at the end, then you're done
    if current_path[-1] == "end":
        return [current_path]

    # Otherwise...
    # - Determine valid routes out of current location
    possible_next_locations = find_possible_next_locations(puzzle_input, current_path, part2)

    # - Recursively find paths including each of the valid routes out of the current location
    paths = []
    for loc in possible_next_locations:
        new_path = current_path + [loc]
        paths_with_loc = extend_path(puzzle_input, new_path, part2)
        paths.extend(paths_with_loc)

    return paths


def part1(puzzle_input: List[List[str]]) -> int:
    paths = extend_path(puzzle_input, ["start"])
    return len(paths)


# Part 2
def can_go_small_cave(loc: str, current_path: List[str]) -> bool:
    # If it's not a small cave, it doesn't matter
    if not is_small_cave(loc):
        return False
    
    # If you haven't been before, you can go!
    if loc not in current_path:
        return True

    # Otherwise, logic for cave visits
    small_caves_visited = set([x for x in current_path if is_small_cave(x)])
    max_small_cave_visits = max([current_path.count(s) for s in small_caves_visited])
    if max_small_cave_visits >= 2:
        return False
    return True


def part2(puzzle_input: List[List[str]]) -> int:
    paths = extend_path(puzzle_input, ["start"], part2=True)
    return len(paths)


with open("./Day12Input.txt") as f:
    puzzle_input = [set(x.strip().split("-")) for x in f.readlines()]

print(part1(puzzle_input))
print(part2(puzzle_input))

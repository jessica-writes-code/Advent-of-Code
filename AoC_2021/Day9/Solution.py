from typing import List, Tuple, Set

import numpy as np


# Part 1
def find_low_points(puzzle_input: np.ndarray) -> np.ndarray:
    above = puzzle_input[1:, :] < puzzle_input[0:-1, :]
    above = np.vstack([np.ones((1, above.shape[1]), dtype=bool), above])

    below = puzzle_input[0:-1, :] < puzzle_input[1:, :]
    below = np.vstack([below, np.ones((1, below.shape[1]), dtype=bool)])

    right = puzzle_input[:, 0:-1] < puzzle_input[:, 1:]
    right = np.concatenate((right, np.ones((right.shape[0], 1), dtype=bool)), 1)

    left = puzzle_input[:, 1:] < puzzle_input[:, 0:-1]
    left = np.concatenate((np.ones((left.shape[0], 1), dtype=bool), left), 1)

    return above & below & left & right


def part1(puzzle_input: np.ndarray) -> int:
    low_points = find_low_points(puzzle_input)
    low_point_values = puzzle_input[low_points]
    return np.sum(low_point_values) + len(low_point_values)


# Part 2
def find_adjacent_points(
    x: int, y: int, max_x: int, max_y: int
) -> Set[Tuple[int, int]]:
    potential_adjacent_points = set([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    adjacent_points = set()
    for pair in potential_adjacent_points:
        x_pair, y_pair = pair
        if 0 <= x_pair <= max_x and 0 <= y_pair <= max_y:
            adjacent_points.add(pair)
    return adjacent_points


def find_basin_around(puzzle_input: np.ndarray, x: int, y: int) -> Set[Tuple[int, int]]:
    adjacent_points = find_adjacent_points(
        x, y, puzzle_input.shape[0]-1, puzzle_input.shape[1]-1
    )
    basin_points = {(x, y)}
    for point in adjacent_points:
        if (
            puzzle_input[point[0]][point[1]] != 9
            and puzzle_input[point[0]][point[1]] > puzzle_input[x][y]
        ):
            new_basin_points = find_basin_around(puzzle_input, point[0], point[1])
            basin_points = basin_points.union(new_basin_points)
    return basin_points


def find_basins(puzzle_input: np.ndarray) -> np.ndarray:
    low_points = find_low_points(puzzle_input)
    low_point_positions = [
        x for x in zip(np.where(low_points)[0], np.where(low_points)[1])
    ]
    basins = []
    for x, y in low_point_positions:
        basin = find_basin_around(puzzle_input, x, y)
        basins.append(basin)
    return basins


def part2(puzzle_input: np.ndarray) -> np.ndarray:
    basins = find_basins(puzzle_input)
    basin_lengths = sorted([len(x) for x in basins], key=lambda x: -x)
    return basin_lengths[0] * basin_lengths[1] * basin_lengths[2]


with open("./Day9Input.txt") as f:
    puzzle_input = [list(x.strip()) for x in f.readlines()]
puzzle_input = np.array(puzzle_input).astype(float)

print(part1(puzzle_input))
print(part2(puzzle_input))

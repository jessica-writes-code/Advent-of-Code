from typing import List, Tuple

import numpy as np

# Part 1
def get_adjacent(x: int, y: int, max_x: int, max_y: int) -> List[Tuple[int, int]]:
    adjacent = []
    for x_delta in [-1, 0, 1]:
        for y_delta in [-1, 0, 1]:
            new_x = x + x_delta
            new_y = y + y_delta
            if 0 <= new_x <= max_x and 0 <= new_y <= max_y and (new_x, new_y) != (x, y):
                adjacent.append((new_x, new_y))
    return adjacent


def execute_flashes_around(
    x: int,
    y: int,
    puzzle_input: np.ndarray,
    has_flashed: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:

    # This (x, y) point is non-flashy
    if puzzle_input[x][y] <= 9 or has_flashed[x][y]:
        return puzzle_input, has_flashed

    # This (x, y) point is flashy, so...
    # - Record the flash
    has_flashed[x][y] = True

    # - +1 all adjacent
    adjacent = get_adjacent(x, y, puzzle_input.shape[0] - 1, puzzle_input.shape[1] - 1)
    for x_adj, y_adj in adjacent:
        puzzle_input[x_adj][y_adj] += 1

        # - execute flashes, with updated state
        puzzle_input, has_flashed = execute_flashes_around(
            x_adj, y_adj, puzzle_input, has_flashed
        )

    return puzzle_input, has_flashed


def part1(puzzle_input: np.ndarray, steps: int) -> int:
    num_flashes = 0
    for _ in range(steps):
        puzzle_input += 1
        has_flashed = np.zeros_like(puzzle_input, dtype=bool)
        for x in range(puzzle_input.shape[0]):
            for y in range(puzzle_input.shape[1]):
                puzzle_input, has_flashed = execute_flashes_around(
                    x, y, puzzle_input, has_flashed
                )
        puzzle_input = puzzle_input * (1-has_flashed)
        num_flashes += np.sum(has_flashed)
    return num_flashes


# Part 2
def part2(puzzle_input: np.ndarray) -> int:
    step = 0
    simultaneous_flash = False
    while not simultaneous_flash:
        puzzle_input += 1
        has_flashed = np.zeros_like(puzzle_input, dtype=bool)
        for x in range(puzzle_input.shape[0]):
            for y in range(puzzle_input.shape[1]):
                puzzle_input, has_flashed = execute_flashes_around(
                    x, y, puzzle_input, has_flashed
                )
        puzzle_input = puzzle_input * (1-has_flashed)
        simultaneous_flash = has_flashed.all()
        step += 1
    return step + 1


with open("./Day11Input.txt") as f:
    puzzle_input = [list(x.strip()) for x in f.readlines()]
puzzle_input = np.array(puzzle_input, dtype=int)

print(part1(puzzle_input, steps=100))
print(part2(puzzle_input))

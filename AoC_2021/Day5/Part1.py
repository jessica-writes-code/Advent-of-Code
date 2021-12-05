from typing import Tuple

import numpy as np


# Load line info
with open("./Day5Input.txt") as f:
    input = [x.strip().split(" -> ") for x in f.readlines()]

line_tuples = [(x[0].split(","), (x[1].split(","))) for x in input]
line_tuples = [
    ((int(x[0][0]), int(x[0][1])), (int(x[1][0]), int(x[1][1]))) for x in line_tuples
]

# Empty grid
size = max([z for x in line_tuples for y in x for z in y])
grid = np.zeros((size + 1, size + 1))

# Fill empty grid
line_tuples_sub = [
    x for x in line_tuples
    if x[0][0] == x[1][0] or x[0][1] == x[1][1]
]  # limit to horizontal/vertical

def grid_fill(grid: np.array, start: Tuple[int, int], end: Tuple[int, int]):
    if start[0] == end[0]:
        j = start[0]
        i_start = min(start[1], end[1])
        i_end = max(start[1], end[1])
        while i_start != i_end + 1:
            grid[i_start][j] += 1
            i_start += 1

    else:
        i = start[1]
        j_start = min(start[0], end[0])
        j_end = max(start[0], end[0])
        while j_start != j_end + 1:
            grid[i][j_start] += 1
            j_start += 1

    return grid


for point_pair in line_tuples_sub:
    start, end = point_pair
    grid = grid_fill(grid, start, end)

print(len(np.where(grid > 1)[0]))

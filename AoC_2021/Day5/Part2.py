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
def grid_fill(grid: np.array, start: Tuple[int, int], end: Tuple[int, int]):
    j_start, i_start = start
    grid[i_start][j_start] += 1

    j_end, i_end = end

    while i_start != i_end or j_start != j_end:
        if i_start != i_end:
            if i_start < i_end:
                i_start += 1
            else:
                i_start -= 1

        if j_start != j_end:
            if j_start < j_end:
                j_start += 1
            else:
                j_start -= 1
        
        grid[i_start][j_start] += 1

    return grid

for point_pair in line_tuples:
    start, end = point_pair
    grid = grid_fill(grid, start, end)

print(len(np.where(grid > 1)[0]))

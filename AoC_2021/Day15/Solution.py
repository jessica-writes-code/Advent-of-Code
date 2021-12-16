import heapq
from typing import List, Tuple
import sys

import numpy as np


def solve(risk_levels: np.ndarray, part2=False) -> int:

    if part2:
        tiles = []
        for i in range(5):
            tiles_i = []
            for j in range(5):
                tile_i_j = risk_levels + i + j
                tile_i_j = tile_i_j % 9
                tile_i_j[tile_i_j == 0] = 9 
                tiles_i.append(tile_i_j)
            tiles.append(np.hstack(tiles_i))
        risk_levels = np.vstack(tiles)

    lowest_costs = np.ones_like(risk_levels) * sys.maxsize
    lowest_costs[0][0] = 0
    queue = []
    heapq.heappush(queue, (0, 0, 0))
    while True:
        _, x, y = heapq.heappop(queue)
        c = lowest_costs[y][x]
        if y == len(risk_levels) - 1 and x == len(risk_levels[y]) - 1:
            return c
        for x1, y1 in ((x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)):
            if y1 not in range(risk_levels.shape[1]) or x1 not in range(risk_levels.shape[0]):
                continue
            d = c + risk_levels[y1][x1]
            if d < lowest_costs[y1][x1]:
                lowest_costs[y1][x1] = d
                heapq.heappush(queue, (d, x1, y1))


with open("./Day15Input.txt") as f:
    puzzle_input = [list(x.strip()) for x in f.readlines()]
risk_levels = np.array(puzzle_input, dtype=int)

print(solve(risk_levels))
print(solve(risk_levels, part2=True))

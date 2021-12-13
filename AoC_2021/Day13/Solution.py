from typing import List, Tuple

import numpy as np
np.set_printoptions(linewidth=np.inf)


def process_input(input: List[str]) -> Tuple[np.ndarray, List[str]]:
    # Split input into array & instructions
    line_ctr, array_coords, instructions = 0, [], []
    while input[line_ctr] != '':
        tmp = input[line_ctr].split(",")
        array_coords.append((int(tmp[0]), int(tmp[1])))
        line_ctr += 1
    line_ctr += 1
    while line_ctr < len(input):
        instructions.append(input[line_ctr].replace("fold_along ", ""))
        line_ctr +=1 

    # Create grid
    horizontal_max = max([x[0] for x in array_coords]) + 1
    vertical_max = max([x[1] for x in array_coords]) + 1
    grid = np.zeros((horizontal_max, vertical_max), dtype=bool)
    for x, y in array_coords:
        grid[x][y] = True

    return grid, instructions


# Part 1
def execute_instructions(grid: np.ndarray, instructions: List[str]) -> np.ndarray:
    for instruction in instructions:
        if instruction.startswith("fold along y="):
            flip_location = int(instruction.replace("fold along y=", ""))
            grid1, grid2 = grid[:,:flip_location], grid[:,flip_location+1:]
            grid_updated = grid1 + np.flip(grid2, 1)
        else:
            flip_location = int(instruction.replace("fold along x=", ""))
            grid1, grid2 = grid[:flip_location,:], grid[flip_location+1:,:]
            grid_updated = grid1 + np.flip(grid2, 0)
        grid = grid_updated

    return grid
    

def part1(grid: np.ndarray, instructions: List[str]) -> int:
    grid_updated = execute_instructions(grid, [instructions[0]])
    return np.sum(grid_updated)


# Part 2
def part2(grid: np.ndarray, instructions: List[str]) -> np.ndarray:
    grid_updated = execute_instructions(grid, instructions)
    grid_updated = grid_updated.astype(str)
    grid_updated[grid_updated == 'True'] = '#'
    grid_updated[grid_updated == 'False'] = ' '
    return grid_updated.transpose()


with open("./Day13Input.txt") as f:
    puzzle_input = [x.strip() for x in f.readlines()]
grid, instructions = process_input(puzzle_input)

print(part1(grid, instructions))
print(part2(grid, instructions))

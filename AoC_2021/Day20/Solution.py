from typing import List, Tuple

import numpy as np
from scipy.signal import convolve2d


def parse_input(puzzle_input: List[str]) -> Tuple[List[int], np.ndarray]:
    algorithm = np.array([1 if x == '#' else 0 for x in list(puzzle_input[0])])
    image = np.vstack(
        [np.array([1 if y == '#' else 0 for y in x])
         for x in puzzle_input[2:]]
    )
    return algorithm, image


def enhance_image(image: List[List[int]], algorithm: List[int], steps: int):
    kernel = 2**np.arange(9).reshape(3,3)
    for i in range(steps):
        fill_value = 0
        if algorithm[0] == 1:
            fill_value = i % 2
        convolved = convolve2d(image, kernel, mode='full', fillvalue=fill_value)
        image = algorithm[convolved]
    return image


with open('Day20Input.txt') as f:
    puzzle_input = [x.strip() for x in f.readlines()]
algorithm, image = parse_input(puzzle_input)

print(np.sum(enhance_image(image, algorithm, 2)))
print(np.sum(enhance_image(image, algorithm, 50)))

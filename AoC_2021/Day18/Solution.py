import json
from typing import List


def find_magnitude(snailfish_number: List) -> int:
    if isinstance(snailfish_number, int):
        return snailfish_number

    if (
        isinstance(snailfish_number, list)
        and isinstance(snailfish_number[0], int)
        and isinstance(snailfish_number[1], int)
    ):
        return snailfish_number[0] * 3 + snailfish_number[1] * 2

    return (
        find_magnitude(snailfish_number[0]) * 3
        + find_magnitude(snailfish_number[1]) * 2
    )


with open("./Day18Input.txt") as f:
    puzzle_input = f.read().strip()

print(find_magnitude(json.loads(puzzle_input)))

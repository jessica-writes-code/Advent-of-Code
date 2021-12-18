import json
from typing import List, Tuple


def find_next_num_loc(snailfish_number: str, backward=False):
    start, end, step = 0, len(snailfish_number), 1
    if backward:
        start, end, step = len(snailfish_number) - 1, 0, -1
    for i in range(start, end, step):
        el = snailfish_number[i]
        if el.isnumeric():
            return i


def explode(snailfish_number: str) -> Tuple[int, int]:
    open_brackets_count = 0
    for i, el in enumerate(snailfish_number):
        if el == '[':
            open_brackets_count += 1
            if open_brackets_count == 5:
                if snailfish_number[i + 1].isnumeric():
                    idx_s, idx_e = i, i + 5
                    pre, post = snailfish_number[:idx_s], snailfish_number[idx_e:]
                    x, y = json.loads(snailfish_number[idx_s: idx_e])

                    left_num_loc = find_next_num_loc(pre, backward=True)
                    if left_num_loc is not None:
                        new_num = x + int(pre[left_num_loc])
                        pre = pre[0:left_num_loc] + str(new_num) + pre[left_num_loc+1:]
                    
                    right_num_loc = find_next_num_loc(post)
                    if right_num_loc is not None:
                        new_num = y + int(post[right_num_loc])
                        post = post[0:right_num_loc] + str(new_num) + post[right_num_loc+1:]

                    snailfish_number = pre + '0' + post
                    return snailfish_number
        
        elif el == ']':
            open_brackets_count -= 1


def snailfish_reduce(snailfish_number: str) -> str:
    while True:
        # If any pair is nested inside four pairs
        snailfish_number = explode(snailfish_number)
        return snailfish_number


def snailfish_addition(to_add: List[str]) -> str:
    current_number = ''
    for i, el in enumerate(to_add):
        current_number += ','
        current_number += el
        if i == 0:
            current_number = current_number[1:]
            continue

        current_number = snailfish_reduce(current_number)

    import pdb
    pdb.set_trace()


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
    puzzle_input = [x.strip() for x in f.readlines()]

print(snailfish_reduce(puzzle_input[0]))

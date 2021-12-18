import itertools
import json
from typing import List, Tuple


def find_next_num_loc(snailfish_number: str, backward=False):
    start, end, step = 0, len(snailfish_number), 1
    if backward:
        start, end, step = len(snailfish_number) - 1, 0, -1
    for i in range(start, end, step):
        el = snailfish_number[i]
        if el.isnumeric():
            if backward is False:
                j = i
                while snailfish_number[j].isnumeric():
                    j += 1
            else:
                j = i + 1
                while snailfish_number[i - 1].isnumeric():
                    i -= 1
            return i, j


def sf_explode(snailfish_number: str) -> str:
    open_brackets_count = 0
    for i, el in enumerate(snailfish_number):
        if el == "[":
            open_brackets_count += 1
            if open_brackets_count == 5:
                if snailfish_number[i + 1].isnumeric():
                    idx_s, idx_e = i, snailfish_number.find("]", i) + 1
                    pre, post = snailfish_number[:idx_s], snailfish_number[idx_e:]
                    x, y = json.loads(snailfish_number[idx_s:idx_e])

                    left_num_loc = find_next_num_loc(pre, backward=True)
                    if left_num_loc is not None:
                        new_num = x + int(pre[left_num_loc[0]:left_num_loc[1]])
                        pre = (
                            pre[0:left_num_loc[0]] + str(new_num) + pre[left_num_loc[1] :]
                        )

                    right_num_loc = find_next_num_loc(post)
                    if right_num_loc is not None:
                        new_num = y + int(post[right_num_loc[0]:right_num_loc[1]])
                        post = (
                            post[0:right_num_loc[0]]
                            + str(new_num)
                            + post[right_num_loc[1] :]
                        )

                    snailfish_number = pre + "0" + post
                    return snailfish_number
        elif el == "]":
            open_brackets_count -= 1
    return snailfish_number


def sf_split(snailfish_number: str) -> str:
    for i, el in enumerate(snailfish_number[0:-1]):
        # If we have at least a 2-digit number
        if el.isnumeric() and snailfish_number[i + 1].isnumeric():
            next_spot = [snailfish_number[i:].find("]"), snailfish_number[i:].find(",")]
            idx_s, idx_e = (
                i,
                i + min([x for x in next_spot if x != -1]),
            )
            pre, post = snailfish_number[:idx_s], snailfish_number[idx_e:]
            num = int(snailfish_number[idx_s: idx_e])
            num_split = [round(num / 2 - 0.05), round(num / 2 + 0.05)]
            return pre + json.dumps(num_split).replace(" ", "") + post
    return snailfish_number


def snailfish_reduce(snailfish_number: str) -> str:
    while True:
        # Explosion
        new_snailfish_number = sf_explode(snailfish_number)

        # If there was an effect, restart the process
        # "you must repeatedly do the first action in this list that applies to the snailfish number"
        if new_snailfish_number != snailfish_number:
            snailfish_number = new_snailfish_number
            continue

        # Split
        new_snailfish_number = sf_split(new_snailfish_number)

        # If there was no effect, you're done
        # "Once no action in the above list applies, the snailfish number is reduced."
        if new_snailfish_number == snailfish_number:
            break

        snailfish_number = new_snailfish_number
    return snailfish_number


def snailfish_addition(to_add: List[str]) -> str:
    current_number = ""
    for i, el in enumerate(to_add):
        current_number += ","
        current_number += el
        if i == 0:
            current_number = current_number[1:]
            continue
        else:
            current_number = "[" + current_number + "]"
        current_number = snailfish_reduce(current_number)
    return current_number


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


def find_max_magnitude(to_add: List[str]) -> int:
    magnitudes = []
    for x, y in itertools.permutations(to_add, 2):
        mag = find_magnitude(json.loads(snailfish_addition([x, y])))
        magnitudes.append(mag)
    return max(magnitudes)


with open("./Day18Input.txt") as f:
    puzzle_input = [x.strip() for x in f.readlines()]

print(find_magnitude(json.loads(snailfish_addition(puzzle_input))))
print(find_max_magnitude(puzzle_input))

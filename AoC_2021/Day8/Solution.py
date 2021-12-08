from collections import defaultdict
from typing import Dict, List, Set


# Part 1
def get_num_part1(code: str) -> int:
    if len(code) == 2:
        return 1
    elif len(code) == 3:
        return 7
    elif len(code) == 4:
        return 4
    elif len(code) == 7:
        return 8
    return None

def part1(puzzle_input: List[List[str]]):
    nums_dict = defaultdict(int)
    for record in puzzle_input:
        for code in record[1]:
            num = get_num_part1(code)
            if num is not None:
                nums_dict[num] += 1
    return sum(nums_dict.values())


# Part 2
def get_overlap(codes_dict: Dict[int, Set[str]], code: str):
    code_set1 = set(code)
    overlap_dict = defaultdict(lambda: None)
    for k, v in codes_dict.items():
        overlap_count = []
        for c in v:
            code_set2 = set(c)
            overlap_count.append(len(code_set1.intersection(code_set2)))
        assert min(overlap_count) == max(overlap_count)
        overlap_dict[k] = min(overlap_count)
    return overlap_dict

def get_decoder_part2(input_codes: List[str]):

    input_codes_dict = defaultdict(set)
    for c in input_codes:
        num = get_num_part1(c)
        if num is not None:
            input_codes_dict[num].add(c)

    def inner(output_code: str):
        overlaps_dict = get_overlap(input_codes_dict, output_code)
        if get_num_part1(output_code) is not None:
            return get_num_part1(output_code)
        elif len(output_code) == 6:  # 0, 6, 9
            if overlaps_dict[1] == 1:
                return 6
            if overlaps_dict[4] == 4:
                return 9
            return 0
        elif len(output_code) == 5:  # 2, 3, 5
            if overlaps_dict[7] == 3:
                return 3
            if overlaps_dict[4] == 3:
                return 5
            return 2

    return inner

def part2(puzzle_input: List[List[str]]):
    results = []
    for record in puzzle_input:
        decoder = get_decoder_part2(record[0])
        result = ''
        for code in record[1]:
            result += str(decoder(code))
        results.append(int(result))
    return sum(results)


with open("./Day8Input.txt") as f:
    puzzle_input = [x.strip().split(" | ") for x in f.readlines()]
    puzzle_input = [(x[0].split(" "), x[1].split(" ")) for x in puzzle_input]

print(part1(puzzle_input))
print(part2(puzzle_input))

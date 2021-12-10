from typing import List, Optional

charmap = {"(": ")", "[": "]", "{": "}", "<": ">"}
charmap_rev = {v: k for k, v in charmap.items()}

charvals = {")": 3, "]": 57, "}": 1197, ">": 25137}
charvals_completion = {")": 1, "]": 2, "}": 3, ">": 4}

# Part 1
def find_first_illegal_char(line: List[str]) -> Optional[str]:
    tracker = []
    for char in line:
        if char in ["(", "[", "{", "<"]:
            tracker.append(char)
        elif char in [")", "]", "}", ">"]:
            if tracker[-1] == charmap_rev[char]:
                tracker.pop()
            else:
                return char
        else:
            raise ValueError
    return None


def part1(puzzle_input: List[List[str]]) -> int:
    total = 0
    for line in puzzle_input:
        first_illegal_char = find_first_illegal_char(line)
        if first_illegal_char is not None:
            total += charvals[first_illegal_char]
    return total


# Part 2
def find_completion_string(line: List[str]) -> List[str]:
    # Find (completion) status at end of line
    tracker = []
    for char in line:
        if char in ["(", "[", "{", "<"]:
            tracker.append(char)
        elif char in [")", "]", "}", ">"]:
            last_char = tracker.pop()
            assert last_char == charmap_rev[char]
        else:
            raise ValueError

    # Find string to complete the line
    completion_string = []
    for char in tracker[::-1]:
        completion_string.append(charmap[char])

    return completion_string


def score_completion_string(string: List[str]) -> int:
    # Find the score for a completion string
    score = 0
    for char in string:
        score = score * 5
        score += charvals_completion[char]
    
    return score


def part2(puzzle_input: List[List[str]]) -> int:
    scores = []
    for line in puzzle_input:
        first_illegal_char = find_first_illegal_char(line)
        if first_illegal_char is not None:
            continue
        completion_string = find_completion_string(line)
        score = score_completion_string(completion_string)
        scores.append(score)
    
    return sorted(scores)[len(scores) // 2]


with open("./Day10Input.txt") as f:
    puzzle_input = [list(x.strip()) for x in f.readlines()]

print(part1(puzzle_input))
print(part2(puzzle_input))

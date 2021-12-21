import itertools
from typing import Dict, List, Tuple


# Part 1
def find_die_outcome(i: int, die_max: int) -> List[int]:
    outcomes = []
    for _ in range(3):
        if i == 0:
            outcomes.append(die_max)
        else:
            outcomes.append(i)
        i += 1
        i = i % die_max
    return outcomes, i


def update_game(die_outcome: List[int], player_location: int, player_score: int):
    s = sum(die_outcome)
    location = player_location + s
    location = location % 10
    if location == 0:
        location = 10
    score = player_score + location
    return location, score


def find_end_conditions(start_player1: int, start_player2: int) -> Tuple[int, int, int]:
    """Output is end-score player1, end-score player 2, num times die rolled"""
    player1_location, player2_location = start_player1, start_player2
    player1_score, player2_score = 0, 0
    i, turn, num_times_rolled = 1, 1, 0
    while max(player1_score, player2_score) < 1000:
        die_outcome, i = find_die_outcome(i, 100)
        num_times_rolled += 3
        if turn == 1:
            player1_location, player1_score = update_game(
                die_outcome, player1_location, player1_score
            )
            turn = 2
        elif turn == 2:
            player2_location, player2_score = update_game(
                die_outcome, player2_location, player2_score
            )
            turn = 1

    return player1_score, player2_score, num_times_rolled


def part1(player1_start: int, player2_start: int) -> int:
    player1_score, player2_score, num_times_rolled = find_end_conditions(
        player1_start, player2_start
    )
    return min(player1_score, player2_score) * num_times_rolled


# Part 2
def find_times_won(
    player1_start: int,
    player1_score: int,
    player2_start: int,
    player2_score: int,
    next_player: int,
    cache: Dict[Tuple[int, int, int, int], int]
) -> int:
    if player1_score >= 21:
        return 1, 0
    elif player2_score >= 21:
        return 0, 1
    elif (player1_start, player1_score, player2_start, player2_score, next_player) in cache:
        return cache[(player1_start, player1_score, player2_start, player2_score, next_player)]

    outcomes = []
    for next3rolls in itertools.product(range(1, 4), repeat=3):
        if next_player == 1:
            new_player1_start, new_player1_score = update_game(
                next3rolls, player1_start, player1_score
            )
            new_outcomes = find_times_won(
                new_player1_start, new_player1_score, player2_start, player2_score, 2, cache
            )
        elif next_player == 2:
            new_player2_start, new_player2_score = update_game(
                next3rolls, player2_start, player2_score
            )
            new_outcomes = find_times_won(
                player1_start, player1_score, new_player2_start, new_player2_score, 1, cache
            )
        outcomes.append(new_outcomes)
    result = (sum([x[0] for x in outcomes]), sum([x[1] for x in outcomes]))
    cache[(player1_start, player1_score, player2_start, player2_score, next_player)] = result
    return result


def part2(player1_start: int, player2_start: int) -> int:
    player1_wins, player2_wins = find_times_won(player1_start, 0, player2_start, 0, 1, {})
    return player1_wins, player2_wins


print(part1(10, 2))
print(part2(10, 2))

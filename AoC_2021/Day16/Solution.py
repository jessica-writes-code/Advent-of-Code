from typing import List, Optional, Tuple

import numpy as np

# Maps
hex_to_binary_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hex_to_binary(str) -> str:
    list_of_str = list(str)
    new_list = []
    for char in list_of_str:
        new_list.append(hex_to_binary_map[char])
    return "".join(new_list)


def parse_literal(literal: str) -> int:
    groups, is_end = [], False
    while not is_end:
        segment = literal[0:5]
        literal = literal[5:]
        if int(segment[0]) == 0:
            is_end = True
        groups.append(segment[1:])
    return int("".join(groups), 2), literal


def parse_operator(packet: str, length_type_id: int):
    if length_type_id == 0:
        length_of_subpackets = int(packet[0:15], 2)
        packet = packet[15:]
        contents, _ = parse_packets(packet[0:length_of_subpackets])
        packet = packet[length_of_subpackets:]
    elif length_type_id == 1:
        number_of_subpackets = int(packet[0:11], 2)
        packet = packet[11:]
        contents, packet = parse_packets(packet, number_of_subpackets)
    else:
        raise ValueError

    return contents, packet


def get_numeric_prefix(packet: str, num_chars: int) -> Tuple[int, str]:
    chars = packet[0:num_chars]
    return int(chars, 2), packet[num_chars:]


def parse_packets(packet: str, total_num_packets: int = None):
    parsed_packets, is_end = [], False
    while not is_end:
        version, packet = get_numeric_prefix(packet, 3)
        type_id, packet = get_numeric_prefix(packet, 3)

        if type_id == 4:
            content, packet = parse_literal(packet)
        else:
            length_type_id, packet = get_numeric_prefix(packet, 1)
            content, packet = parse_operator(packet, length_type_id)

        parsed_packets.append((version, type_id, content))

        if (
            len(parsed_packets) == total_num_packets
            or len(packet.replace("0", "")) == 0
        ):
            is_end = True

    return parsed_packets, packet


def part1(puzzle_input):
    parsed_packet, _ = parse_packets(hex_to_binary(puzzle_input), 1)
    version_numbers = []
    while len(parsed_packet) > 0:
        el = parsed_packet.pop()
        version_numbers.append(el[0])
        if isinstance(el[2], list):
            parsed_packet.extend(el[2])
    return sum(version_numbers)


def perform_operations(parsed_packet):
    type_id = parsed_packet[1]

    if type_id == 4:
        return parsed_packet[2]

    values = []
    for el in parsed_packet[2]:
        values.append(perform_operations(el))
    
    print(values)
    if type_id == 0:
        return sum(values)
    if type_id == 1:
        return np.prod(values)
    if type_id == 2:
        return min(values)
    if type_id == 3:
        return max(values)
    if type_id == 5:
        return values[0] > values[1]
    if type_id == 6:
        return values[0] < values[1]
    if type_id == 7:
        return values[0] == values[1]


def part2(puzzle_input):
    parsed_packet, _ = parse_packets(hex_to_binary(puzzle_input), 1)
    return perform_operations(parsed_packet[0])


with open("./Day16Input.txt") as f:
    puzzle_input = f.read().strip()

print(part1(puzzle_input))
print(part2(puzzle_input))

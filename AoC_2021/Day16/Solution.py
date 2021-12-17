from typing import Optional

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
binary_to_hex_map = {v: k for k, v in hex_to_binary_map.items()}


def hex_to_binary(str) -> str:
    list_of_str = list(str)
    new_list = []
    for char in list_of_str:
        new_list.append(hex_to_binary_map[char])
    return "".join(new_list)


def get_possible_numbers(binary_str: str):
    possible_literals = []
    for k, v in binary_to_hex_map.items():
        k_lstrip = k.lstrip("0")
        if len(k_lstrip) > 0 and binary_str.startswith(k_lstrip):
            try:
                float(v)
                possible_literals.append((v, k_lstrip))
            except:
                pass
    return possible_literals


def get_literal(binary_str: str) -> Optional[str]:

    # Divide into groups of 5 bits
    bit_segments = []
    for i in range(0, len(binary_str), 5):
        bit_segments.append(binary_str[i:i+5])

    # Remove final segment if it's buffer
    if len(bit_segments[-1]) < 5:
        bit_segments.pop()

    # Parse divided segments into literal values
    literal_segments = []
    for i, segment in enumerate(bit_segments):
        if i == len(bit_segments) - 1:
            # Anything other than 0s in a non-5-bit final segment
            if len(segment) < 5 and '1' in segment:
                return None

            # Final segment doesn't start with 0
            if not segment.startswith('0'):
                return None

        else:
            # Non-final segment doesn't start with 1
            if not segment.startswith('1'):
                return None 

        literal_segments.append(segment[1:])

    literal = ''.join(literal_segments)
    return int(literal, 2)


def parse_packet(
    packet: str,
    version: Optional[str] = None,
    type_id: Optional[str] = None,
    value: Optional[str] = None,
):

    # If no version has been identified yet...
    if version is None:
        for v_hex, v_binary in get_possible_numbers(packet):
            packet_substr = packet[len(v_binary) :]
            version, type_id, value = parse_packet(packet_substr, version=v_hex)
            if value is not None:
                break
        return version, type_id, value

    if type_id is None:
        for t_hex, t_binary in get_possible_numbers(packet):
            packet_substr = packet[len(t_binary) :]
            version, type_id, value = parse_packet(
                packet_substr, version=version, type_id=t_hex
            )
            if value is not None:
                break
        return version, type_id, value

    value = get_literal(packet)
    return version, type_id, value


def part1(puzzle_input: str) -> int:
    binary_representation = hex_to_binary(puzzle_input)
    version, type_id, value = parse_packet(binary_representation)
    import pdb

    pdb.set_trace()


with open("./Day16Input.txt") as f:
    puzzle_input = f.read().strip()

print(part1(puzzle_input))

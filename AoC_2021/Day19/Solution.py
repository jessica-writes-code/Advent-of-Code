from __future__ import annotations
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
import itertools
from math import sqrt
from typing import Any, Dict, List, Optional, Set, Tuple


REQUIRED_OVERLAP = 12
TRANSFORMS = [
    (i, j, k, r1, r2, r3)
    for i, j, k in itertools.permutations(range(3), 3)
    for r1, r2, r3 in itertools.product((-1, 1), repeat=3)
]


def transformation_of(
    beacon: Beacon, by: Tuple[int, int, int, int, int, int]
) -> Beacon:
    i, j, k, r1, r2, r3 = by
    beacon_tuple = beacon.to_tuple()
    return Beacon(
        x=r1 * beacon_tuple[i], y=r2 * beacon_tuple[j], z=r3 * beacon_tuple[k]
    )


def get_highest_count_key(x: Dict[Any, int]) -> Any:
    max_k, max_v = None, 0
    for k, v in x.items():
        if v > max_v:
            max_k = k
            max_v = v
    return max_k


@dataclass
class Beacon:
    x: int
    y: int
    z: int

    def to_tuple(self) -> Tuple[int, int, int]:
        return self.x, self.y, self.z

    def distance_to(self, other: Beacon) -> float:
        return sqrt(
            (other.x - self.x) ** 2 + (other.y - self.y) ** 2 + (other.z - self.z) ** 2
        )

    def vector_to(self, other: Beacon) -> Tuple[int, int, int]:
        return (other.x - self.x, other.y - self.y, other.z - self.z)


class Scanner:
    def __init__(self, beacons: Dict[int, Beacon]):
        self.beacons = beacons
        self.beacon_distances = {
            (beacon1_num, beacon2_num): round(beacon1.distance_to(beacon2), 4)
            for beacon1_num, beacon1 in self.beacons.items()
            for beacon2_num, beacon2 in self.beacons.items()
            if beacon1_num != beacon2_num
        }
        self.calibrated = False

    def set_position(self, x: int, y: int, z: int) -> None:
        self.x, self.y, self.z = x, y, z
        self.calibrated = True

    def find_overlapping_beacons(self, other: Scanner):
        # Beacon pair overlap
        beacon_pair_map = {}
        for pair_self, distance_self in self.beacon_distances.items():
            for pair_other, distance_other in other.beacon_distances.items():
                if distance_self == distance_other:
                    beacon_pair_map[pair_self] = pair_other

        # Beacon-to-beacon map
        beacon_count_map = defaultdict(lambda: defaultdict(int))
        for pair_self, pair_other in beacon_pair_map.items():
            beacon_count_map[pair_self[0]][pair_other[0]] += 1
            beacon_count_map[pair_self[0]][pair_other[1]] += 1
            beacon_count_map[pair_self[1]][pair_other[0]] += 1
            beacon_count_map[pair_self[1]][pair_other[1]] += 1

        beacon_map = {}
        for beacon_self, beacon_other_counts in beacon_count_map.items():
            beacon_map[beacon_self] = get_highest_count_key(beacon_other_counts)

        return beacon_map

    def update(self, other: Scanner, matches: Dict[int, int]) -> None:
        # Find the appropriate transformation
        cnt = defaultdict(int)
        for i, transform in enumerate(TRANSFORMS):
            for m1, m2 in itertools.permutations(matches.keys(), 2):
                t_m1 = transformation_of(self.beacons[m1], transform)
                t_m2 = transformation_of(self.beacons[m2], transform)
                v_m1_m2 = t_m1.vector_to(t_m2)

                v_m1_m2_other = other.beacons[matches[m1]].vector_to(
                    other.beacons[matches[m2]]
                )

                if v_m1_m2 == v_m1_m2_other:
                    cnt[i] += 1

        correct_transform = TRANSFORMS[get_highest_count_key(cnt)]

        # Calculate scanner's x, y, z & set it
        for self_id, other_id in matches.items():
            break
        calibrated_scanner_to_beacon = other.beacons[other_id].to_tuple()
        current_scanner_to_beacon = transformation_of(
            self.beacons[self_id], correct_transform
        ).to_tuple()
        current_scanner_location = [
            calibrated_scanner_to_beacon[i] - current_scanner_to_beacon[i]
            for i in range(3)
        ]
        self.set_position(*current_scanner_location)

        # Update beacon locations vis-a-vis Scanner 0
        for i in range(len(self.beacons)):
            if i in matches:
                self.beacons[i] = copy(other.beacons[matches[i]])
            else:
                transformed_beacon = transformation_of(
                    self.beacons[i], correct_transform
                )
                self.beacons[i] = Beacon(
                    transformed_beacon.x + self.x,
                    transformed_beacon.y + self.y,
                    transformed_beacon.z + self.z,
                )

        self.calibrated = True


class Map:
    def __init__(self, scanners: Dict[int, Scanner]):
        self.scanners = scanners

    def fully_calibrated(self) -> bool:
        return min([scanner.calibrated for _, scanner in self.scanners.items()])

    def calibrate_scanners(self):
        # Base all other orientations on the first scanner
        self.scanners[0].set_position(0, 0, 0)
        insufficient_overlap = []
        while not self.fully_calibrated():
            for i, j in itertools.permutations(range(len(self.scanners)), 2):
                if (i, j) in insufficient_overlap:
                    continue
                if self.scanners[i].calibrated and not self.scanners[j].calibrated:
                    overlapping_beacons = self.scanners[j].find_overlapping_beacons(
                        self.scanners[i]
                    )
                    if len(overlapping_beacons) >= REQUIRED_OVERLAP:
                        self.scanners[j].update(self.scanners[i], overlapping_beacons)
                        break
                    else:
                        insufficient_overlap.append((i, j))

    def get_beacons(self):
        # Get a set of the beacons
        beacon_set = set()
        for _, scanner in self.scanners.items():
            new_beacons = set()
            for _, beacon in scanner.beacons.items():
                new_beacons.add(beacon.to_tuple())
            beacon_set = beacon_set.union(new_beacons)
        return beacon_set


# Load data into Beacon, Scanner, Map objects
with open("./Day19Input.txt") as f:
    puzzle_input = [x.strip() for x in f.readlines()] + [""]

scanners, beacons, i = {}, {}, 0
while i in range(len(puzzle_input)):
    input_line = puzzle_input[i]
    if "scanner" in input_line:
        scanner_number = int(input_line.replace("--- scanner ", "").replace(" ---", ""))
    elif "," in input_line:
        x_str, y_str, z_str = input_line.split(",")
        x, y, z = int(x_str), int(y_str), int(z_str)
        beacons[len(beacons)] = Beacon(x, y, z)
    else:
        scanners[scanner_number] = Scanner(beacons=beacons)
        beacons = {}
    i += 1

map_of_scanners = Map(scanners)
map_of_scanners.calibrate_scanners()
print(len(map_of_scanners.get_beacons()))

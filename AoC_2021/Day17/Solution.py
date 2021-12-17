from dataclasses import dataclass
from typing import Tuple


@dataclass
class TargetArea:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def contains(self, x: int, y: int) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def cannot_reach_from(
        self, x: int, y: int, velocity_x: int, velocity_y: int
    ) -> bool:
        return (x > self.x_max) or (y < self.y_min and velocity_y <= 0)


def find_end_point(
    velocity_x: int, velocity_y: int, target_area: TargetArea
) -> Tuple[int, int]:
    x, y, max_y = 0, 0, 0
    while not target_area.contains(x, y) and not target_area.cannot_reach_from(
        x, y, velocity_x, velocity_y
    ):
        x += velocity_x
        y += velocity_y
        if y > max_y:
            max_y = y
        if velocity_x > 0:
            velocity_x -= 1
        elif velocity_x < 0:
            velocity_x += 1
        velocity_y -= 1
    return x, y, max_y


def solve(target_area: TargetArea):
    successes = []
    for velocity_x in range(target_area.x_max + 1):
        for velocity_y in range(target_area.y_min, abs(target_area.y_min)):  # TODO: Fix
            # Get the end point, with this initial x-velocity, y-velocity
            end_point_x, end_point_y, max_y = find_end_point(
                velocity_x, velocity_y, target_area
            )

            # You've made it to the target!
            if target_area.contains(end_point_x, end_point_y):
                successes.append((velocity_x, velocity_y, max_y))

    return max([x[2] for x in successes]), len(successes)   


print(solve(TargetArea(x_min=288, x_max=330, y_min=-96, y_max=-50)))

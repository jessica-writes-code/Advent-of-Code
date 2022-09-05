# Problem: https://adventofcode.com/2019/day/5

from turtle import position
from typing import List


class Day5Solver:
    def __init__(self, file_path: str):
        """Load and parse puzzle input"""
        with open(file_path) as f:
            self.raw_input = [x.strip() for x in f.readlines()]
        self.input = [int(x) for x in self.raw_input[0].split(',')]

    @staticmethod
    def parse_start_value(value: int) -> List[int]:
        """Identify OpCode and modes of parameters"""
        value_str_filled = str(value).zfill(6)
        opcode = int(value_str_filled[-2:])
        modes = [int(x) for x in value_str_filled[-3:0:-1]]
        return opcode, modes

    @staticmethod
    def get_value(entry: int, param_mode: int, values: List[int]) -> int:
        """Get value to be manipulated, according to the parameter mode"""
        # If the OpCode is 0, the system is in position mode
        # If the OpCode is 1, the system is in immediate mode
        # There are no other modes
        if param_mode == 0:
            return values[entry]
        return entry

    def execute_instructions(self, values: List[int], input_value: int) -> int:
        """Apply instructions sequentially to the values, collecting outputs
        along the way"""
        position, outputs = 0, []
        while position <= len(values):

            opcode, modes = self.parse_start_value(values[position])

            # OpCodes 1 and 2 serve to add or multiply (respectively) the next two
            # values and then write the result to the index indicated by the third
            # value.
            # OpCodes 7 and 8 serve to test the direcitonal inequality (<) or equality
            # of two values and then write 0 or 1 into the index indicated by the
            # third value, depending on the outcome of the comparison.
            if opcode in (1, 2, 7, 8):

                val1 = self.get_value(values[position + 1], modes[0], values)
                val2 = self.get_value(values[position + 2], modes[1], values)

                if opcode == 1:
                    val_result = val1 + val2
                elif opcode == 2:
                    val_result = val1 * val2
                elif opcode == 7:
                    val_result = int(val1 < val2)
                elif opcode == 8:
                    val_result = int(val1 == val2)

                values[values[position + 3]] = val_result

                position += 4

            # OpCode 3 serves to take input and write it to the index indicated by the
            # next value. OpCode 4 serves to provide output, as indicated by the next
            # value.
            elif opcode in (3, 4):

                param_val = values[position + 1]

                if opcode == 3:
                    values[param_val] = input_value
                elif opcode == 4:
                    outputs.append(
                        self.get_value(param_val, modes[0], values)
                    )

                position += 2

            # OpCodes 5 and 6 serve to update the location of the pointer to the index
            # indicated by the second paramebter, based on the value of the first
            # parameter.
            elif opcode in (5, 6):

                val1 = self.get_value(values[position + 1], modes[0], values)
                val2 = self.get_value(values[position + 2], modes[1], values)

                if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                    position = val2
                else:
                    position += 3

            # OpCode 99 stops the program
            elif opcode == 99:
                break

            else:
                raise ValueError('Something is wrong!')

        return outputs

    def find_diagnostic_code(self, input_value: int) -> int:

        outputs = self.execute_instructions(self.input.copy(), input_value)
        for output in outputs[0:-1]:
            assert output == 0
        return outputs[-1]

    def solve_part1(self) -> int:
        return self.find_diagnostic_code(1)

    def solve_part2(self) -> int:
        return self.find_diagnostic_code(5)


if __name__ == "__main__":
    solver = Day5Solver("Day5Input.txt")
    print('The solution to part 1 is', solver.solve_part1())
    print('The solution to part 2 is', solver.solve_part2())

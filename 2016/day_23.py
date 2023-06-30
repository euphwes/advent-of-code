from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembunny import AssembunnyInstruction, evaluate_assembunny

DAY = 23
YEAR = 2016

PART_ONE_DESCRIPTION = "value in register a if a starts at 7"
PART_ONE_ANSWER = 12800

PART_TWO_DESCRIPTION = "value in register a if a starts at 12"
PART_TWO_ANSWER = 479009360


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions):
    # Init a register bank a-d to 0 values, except a which is 7
    registers = {x: 0 for x in "abcd"}
    registers["a"] = 7

    for step in iter(evaluate_assembunny(registers, instructions)):
        pass

    return registers["a"]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(instructions):
    # Init a register bank a-d to 0 values, except a which is 12
    registers = {x: 0 for x in "abcd"}
    registers["a"] = 12

    for step in iter(evaluate_assembunny(registers, instructions)):
        pass

    return registers["a"]


# ----------------------------------------------------------------------------------------------


def run(input_file):
    instructions = get_input(input_file)

    part_one([AssembunnyInstruction.from_line(line) for line in instructions])
    part_two([AssembunnyInstruction.from_line(line) for line in instructions])

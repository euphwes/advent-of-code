from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembunny import AssembunnyInstruction, evaluate_assembunny

DAY = 12
YEAR = 2016

PART_ONE_DESCRIPTION = "value in register a"
PART_ONE_ANSWER = 318083

PART_TWO_DESCRIPTION = "value in register a if c starts at 1"
PART_TWO_ANSWER = 9227737


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions):

    # Init a register bank a-d to 0 values
    registers = {x: 0 for x in "abcd"}

    for step in iter(evaluate_assembunny(registers, instructions)):
        pass

    return registers["a"]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(instructions):

    # Init a register bank a-d to 0, except c which is 1
    registers = {x: 0 for x in "abcd"}
    registers["c"] = 1

    for step in iter(evaluate_assembunny(registers, instructions)):
        pass

    return registers["a"]


# ----------------------------------------------------------------------------------------------


def run(input_file):

    instructions = get_input(input_file)

    part_one([AssembunnyInstruction.from_line(line) for line in instructions])
    part_two([AssembunnyInstruction.from_line(line) for line in instructions])

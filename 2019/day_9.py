from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from .intcode import IntcodeComputer

DAY = 9
YEAR = 2019

PART_ONE_DESCRIPTION = "BOOST keycode"
PART_ONE_ANSWER = 2399197539

PART_TWO_DESCRIPTION = "distress signal coordinates"
PART_TWO_ANSWER = 35106


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(program):
    computer = IntcodeComputer()
    computer.execute(program, program_input=[1])

    assert computer.has_output()
    return computer.get_output()


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(program):
    computer = IntcodeComputer()
    computer.execute(program, program_input=[2])

    assert computer.has_output()
    return computer.get_output()


# ----------------------------------------------------------------------------------------------


def run(input_file):
    program = get_tokenized_input(input_file, ",", lambda t: int(t))[0]
    part_one(program)

    program = get_tokenized_input(input_file, ",", lambda t: int(t))[0]
    part_two(program)

from util.input import get_tokenized_input
from util.iter import nested_iterable
from util.decorators import aoc_output_formatter

from .intcode import IntcodeComputer


DAY = 2
YEAR = 2019

PART_ONE_DESCRIPTION = "value at position 0 after program halts"
PART_ONE_ANSWER = 3716250

PART_TWO_DESCRIPTION = "100 * noun + verb"
PART_TWO_ANSWER = 6472


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(program):

    # Override the values in the program at positions 1 and 2 as described
    # by the problem description
    program[1] = 12
    program[2] = 2

    computer = IntcodeComputer()
    computer.execute(program)

    return computer.program[0]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(original_program):

    # We're looking to override the values with position 1 with 'noun' and
    # position 2 with 'verb' such that the program output (the value in
    # position 0 when the program halts) is 19690720
    for noun, verb in nested_iterable(range(100), range(100)):

        # Copy the original program.
        # Set the values at positions 1 and 2 with `noun` and `verb`
        program = [line for line in original_program]
        program[1] = noun
        program[2] = verb

        computer = IntcodeComputer()
        computer.execute(program)

        if computer.program[0] == 19690720:
            return (100 * noun) + verb


# ----------------------------------------------------------------------------------------------


def run(input_file):
    program = get_tokenized_input(input_file, ",", int)[0]
    part_one(program)

    program = get_tokenized_input(input_file, ",", int)[0]
    part_two(program)

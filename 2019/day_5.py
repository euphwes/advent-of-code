from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from .intcode import IntcodeComputer

DAY = 5
YEAR = 2019

PART_ONE_DESCRIPTION = "diagnostic code"
PART_ONE_ANSWER = 13818007

PART_TWO_DESCRIPTION = "diagnostic code"
PART_TWO_ANSWER = 3176266


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(program):
    computer = IntcodeComputer()
    computer.execute(program, program_input=[1])

    # All the output values except the last should be 0, indicating passing tests.
    # The final output is the diagnostic code
    while computer.has_output():
        output = computer.get_output()

    return output


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(program):
    computer = IntcodeComputer()
    computer.execute(program, program_input=[5])

    # All the output values except the last should be 0, indicating passing tests.
    # The final output is the diagnostic code
    while computer.has_output():
        output = computer.get_output()

    return output


# ----------------------------------------------------------------------------------------------


def run(input_file):
    # Transform the input into a list of ints which define the Intcode program
    program = get_tokenized_input(input_file, ",", lambda t: int(t))[0]

    # Copy the program before passing to the computers, so we're not modifying
    # values during part one that break the program in part two.
    copy = lambda program: [x for x in program]
    part_one(copy(program))
    part_two(copy(program))

    # LESS_THAN and EQUALS tests
    # test = [3,9,8,9,10,9,4,9,99,-1,8]  # position mode, output 1 if input is 8, otherwise 0
    # test = [3,9,7,9,10,9,4,9,99,-1,8]  # position mode, output 1 if input < 8, otherwise 0
    # test = [3,3,1108,-1,8,3,4,3,99]    # immediate mode, output 1 if input is 8, otherwise 0
    # test = [3,3,1107,-1,8,3,4,3,99]    # immediate mode, output 1 if input < 8, otherwise 0

    # JUMP tests
    # position mode, output 0 if input = 0, otherwise 1
    # test = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    # immediate mode, output 0 if input = 0, otherwise 1
    # test = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

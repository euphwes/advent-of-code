from itertools import permutations

from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from .intcode import InputNotAvailableException, IntcodeComputer

DAY = 7
YEAR = 2019

PART_ONE_DESCRIPTION = "max thruster signal"
PART_ONE_ANSWER = 19650

PART_TWO_DESCRIPTION = "max thruster signal"
PART_TWO_ANSWER = 35961106


copy = lambda program: [x for x in program]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(input_program):
    max_output_signal = 0
    for phase_sequence in permutations(range(5)):
        signal = 0

        for n in range(5):
            inputs = [phase_sequence[n], signal]

            computer = IntcodeComputer()
            computer.execute(copy(input_program), program_input=inputs)

            signal = computer.get_output()

        max_output_signal = max(max_output_signal, signal)

    return max_output_signal


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(input_program):
    max_output_signal = 0

    for phase_sequence in permutations([9, 8, 7, 6, 5]):
        signal = 0
        amps = [IntcodeComputer() for _ in range(5)]

        complete = False
        while not complete:
            for n in range(5):
                computer = amps[n]
                try:
                    if computer.state == IntcodeComputer.STATE_WAITING:
                        inputs = [signal]
                    else:
                        inputs = [phase_sequence[n], signal]
                    computer.execute(copy(input_program), program_input=inputs)
                except InputNotAvailableException:
                    signal = computer.get_output()
                    continue
                else:
                    signal = computer.get_output()
                    if n == 4:
                        complete = True

        max_output_signal = max(max_output_signal, signal)

    return max_output_signal


# ----------------------------------------------------------------------------------------------


def run(input_file):
    # Transform the input into a list of ints which define the Intcode program
    program = get_tokenized_input(input_file, ",", lambda t: int(t))[0]

    # Copy the program before passing to the computers, so we're not modifying
    # values during part one that break the program in part two.
    part_one(copy(program))
    part_two(copy(program))

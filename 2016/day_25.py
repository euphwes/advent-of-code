from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

from .assembunny import AssembunnyInstruction, evaluate_assembunny

DAY = 25
YEAR = 2016

PART_ONE_DESCRIPTION = "lowest starting value of register a to produce clock signal"
PART_ONE_ANSWER = 158


CLOCK_SIGNAL_VALUES = {0, 1}

CLOCK_SIGNAL_CHECK_LENGTH = 10
LIKELY_CLOCK_SIGNALS = [
    [0, 1] * int(CLOCK_SIGNAL_CHECK_LENGTH / 2),
    [1, 0] * int(CLOCK_SIGNAL_CHECK_LENGTH / 2),
]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions):
    for a_start_value in int_stream():
        # Init an output buffer
        buffer = []

        # Init a register bank a-d to 0 values, except a which is a_start_value
        registers = {x: 0 for x in "abcd"}
        registers["a"] = a_start_value

        for _ in iter(
            evaluate_assembunny(registers, instructions, output_buffer=buffer)
        ):
            if buffer and buffer[-1] not in CLOCK_SIGNAL_VALUES:
                break
            if len(buffer) == CLOCK_SIGNAL_CHECK_LENGTH:
                if any(buffer == signal for signal in LIKELY_CLOCK_SIGNALS):
                    return a_start_value
                else:
                    break


# ----------------------------------------------------------------------------------------------


def run(input_file):
    instructions = [
        AssembunnyInstruction.from_line(line) for line in get_input(input_file)
    ]

    part_one(instructions)

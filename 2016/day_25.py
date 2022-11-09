from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

from .assembunny import evaluate_assembunny, AssembunnyInstruction

#---------------------------------------------------------------------------------------------------

CLOCK_SIGNAL_VALUES = {0, 1}

CLOCK_SIGNAL_CHECK_LENGTH = 10
LIKELY_CLOCK_SIGNALS = [
    [0, 1] * int(CLOCK_SIGNAL_CHECK_LENGTH/2),
    [1, 0] * int(CLOCK_SIGNAL_CHECK_LENGTH/2)
]


@aoc_output_formatter(2016, 25, 1, 'lowest starting value of register a to produce clock signal')
def part_one(instructions):

    for a_start_value in int_stream():

        # Init an output buffer
        buffer = []

        # Init a register bank a-d to 0 values, except a which is a_start_value
        registers = {x: 0 for x in 'abcd'}
        registers['a'] = a_start_value

        for step in iter(evaluate_assembunny(registers, instructions, output_buffer=buffer)):
            if buffer and buffer[-1] not in CLOCK_SIGNAL_VALUES:
                break
            if len(buffer) == CLOCK_SIGNAL_CHECK_LENGTH:
                if any(buffer == signal for signal in LIKELY_CLOCK_SIGNALS):
                    return a_start_value
                else:
                    break

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = [AssembunnyInstruction.from_line(line) for line in get_input(input_file)]

    part_one(instructions)

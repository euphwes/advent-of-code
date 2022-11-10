from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

#---------------------------------------------------------------------------------------------------

def _evaluate_instructions(instructions, offset_modification_rule):
    """ Evaluates a set of instructions, modifying the offset instruction value at the current
    index at each step of the process as described by the rule passed in. Returns the total number
    of steps executed before the current index ends outside of the bounds of the instructions. """

    curr_index = 0
    step_count = 0
    instructions_map = {i: instructions[i] for i in range(len(instructions))}
    while True:
        try:
            offset = instructions_map[curr_index]
            instructions_map[curr_index] = offset_modification_rule(offset)
            curr_index += offset
            step_count += 1
        except KeyError:
            return step_count


@aoc_output_formatter(2017, 5, 1, 'number of steps before instructions exit')
def part_one(instructions):
    rule = lambda x: x+1
    return _evaluate_instructions(instructions, rule)


@aoc_output_formatter(2017, 5, 2, 'number of steps before instructions exit')
def part_two(instructions):
    rule = lambda x: x-1 if x >= 3 else x+1
    return _evaluate_instructions(instructions, rule)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = [line[0] for line in get_tokenized_input(input_file, None, int)]

    part_one(instructions)
    part_two(instructions)

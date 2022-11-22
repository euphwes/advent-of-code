from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembly import evaluate_assembly, evaluate_assembly_v2, AssemblyInstruction

from collections import defaultdict

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2017, 18, 1, 'first recovered frequency')
def part_one(instructions):
    for stepwise_recovered_freq in evaluate_assembly(defaultdict(int), instructions):
        if stepwise_recovered_freq is not None:
            return stepwise_recovered_freq


@aoc_output_formatter(2017, 18, 2, 'number of times program 1 sent a value')
def part_two(instructions):
    prog_a_input = list()
    prog_a_output = list()

    prog_b_input = list()
    prog_b_output = list()

    prog_a = evaluate_assembly_v2(defaultdict(int, p=0), instructions, prog_a_input, prog_a_output)

    prog_b = evaluate_assembly_v2(defaultdict(int, p=1), instructions, prog_b_input, prog_b_output)

    times_prog_b_issued_send = 0

    while True:
        a_is_waiting = next(prog_a)
        b_is_waiting = next(prog_b)

        did_any_send = False

        if prog_a_output:
            did_any_send = True
            prog_b_input.append(prog_a_output.pop(0))

        if prog_b_output:
            did_any_send = True
            times_prog_b_issued_send += 1
            prog_a_input.append(prog_b_output.pop(0))

        if a_is_waiting and b_is_waiting and not did_any_send:
            break

    return times_prog_b_issued_send

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw_instructions = get_input(input_file)
    instructions = [AssemblyInstruction.from_line(line) for line in raw_instructions]

    part_one(instructions)
    part_two(instructions)

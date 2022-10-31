from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembunny import evaluate_assembunny, AssembunnyInstruction

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2016, 12, 1, 'value in register a')
def part_one(instructions):

    # Init a register bank a-d to 0 values
    registers = {x: 0 for x in 'abcd'}

    evaluated_registers = evaluate_assembunny(registers, instructions)
    return evaluated_registers['a']


@aoc_output_formatter(2016, 12, 2, 'value in register a if c starts at 1')
def part_two(instructions):

    # Init a register bank a-d to 0, except c which is 1
    registers = {x: 0 for x in 'abcd'}
    registers['c'] = 1

    evaluated_registers = evaluate_assembunny(registers, instructions)
    return evaluated_registers['a']

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = get_input(input_file)

    part_one([AssembunnyInstruction.from_line(line) for line in instructions])
    part_two([AssembunnyInstruction.from_line(line) for line in instructions])

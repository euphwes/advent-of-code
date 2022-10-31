from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembunny import evaluate_assembunny, AssembunnyInstruction

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2016, 23, 1, 'value in register a')
def part_one(instructions):

    # Init a register bank a-d to 0 values, except a which is 7
    registers = {x: 0 for x in 'abcd'}
    registers['a'] = 7

    evaluated_registers = evaluate_assembunny(registers, instructions)
    return evaluated_registers['a']


@aoc_output_formatter(2016, 23, 2, 'value in register a if c starts at 1')
def part_two(instructions):

    # Init a register bank a-d to 0 values, except a which is 7
    registers = {x: 0 for x in 'abcd'}
    registers['a'] = 12

    evaluated_registers = evaluate_assembunny(registers, instructions)
    return evaluated_registers['a']

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = get_input(input_file)

#     instructions = """cpy 2 a
# tgl a
# tgl a
# tgl a
# cpy 1 a
# dec a
# dec a""".split('\n')

    part_one([AssembunnyInstruction.from_line(line) for line in instructions])
    part_two([AssembunnyInstruction.from_line(line) for line in instructions])

from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _evaluate_assembunny (registers, instructions):
    """ Evaluates a set of assembunny instructions against a set of register values, and returns
    the register values when the instructions terminate. """

    # Init the program counter (pointer to instruction) to 0
    pc = 0

    # While the PC is still pointing to a valid instruction...
    while pc < len(instructions):

        # ... grab that instruction and parse it into the command code, and the provided params
        raw_instruction = instructions[pc].split(' ')
        code = raw_instruction[0]
        params = raw_instruction[1:]

        # Remember if we've already modded the program counter with the jnz instruction
        already_modded_pc = False

        # Evaluate a "jump if not zero" instruction
        if code == 'jnz':
            # Determine the value to check if zero. It's either an integer, or a register reference
            val = params[0]
            if val in 'abcd':
                val = registers[val]
            else:
                val = int(val)

            # If the value is not zero, modify the PC by the value of the second parameter.
            if val != 0:
                pc += int(params[1])
                already_modded_pc = True

        # Evaluate a "increment" instruction
        elif code == 'inc':
            registers[params[0]] += 1

        # Evaluate a "decrement" instruction
        elif code == 'dec':
            registers[params[0]] -= 1

        # Evaluate a "copy" instruction
        elif code == 'cpy':
            src = params[0]
            dst = params[1]

            # If the source value is a register reference, grab the value from that register.
            # Otherwise use the source value as an integer directly.
            if src in 'abcd':
                src = registers[src]
            else:
                src = int(src)

            # Update the destination register with the source value.
            registers[dst] = src

        # If we haven't already modified the PC with a jnz instruction, increment the PC.
        if not already_modded_pc:
            pc += 1

    # Done evaluating the instructions, return the register values.
    return registers


@aoc_output_formatter(2016, 12, 1, 'value in register a')
def part_one(instructions):

    # Init a register bank a-d to 0 values
    registers = {x: 0 for x in 'abcd'}

    evaluated_registers = _evaluate_assembunny(registers, instructions)
    return evaluated_registers['a']


@aoc_output_formatter(2016, 12, 2, 'value in register a if c starts at 1')
def part_two(instructions):

    # Init a register bank a-d to 0, except c which is 1
    registers = {x: 0 for x in 'abcd'}
    registers['c'] = 1

    evaluated_registers = _evaluate_assembunny(registers, instructions)
    return evaluated_registers['a']

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = get_input(input_file)

    part_one(instructions)
    part_two(instructions)

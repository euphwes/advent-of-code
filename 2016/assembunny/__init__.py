from dataclasses import dataclass
from typing import List, Union

#---------------------------------------------------------------------------------------------------

@dataclass
class AssembunnyInstruction:
    code: str
    params: List[Union[str, int]]

    @staticmethod
    def from_line(line: str):
        pieces = line.split(' ')
        return AssembunnyInstruction(code=pieces[0], params=pieces[1:])


def evaluate_assembunny(registers, instructions):
    """ Evaluates a set of assembunny instructions against a set of register values, and returns
    the register values when the instructions terminate. """

    # Init the program counter (pointer to instruction) to 0
    pc = 0

    registers_list = set('abcd')

    # While the PC is still pointing to a valid instruction...
    while pc < len(instructions):
        instruction = instructions[pc]
        params = instruction.params

        # Remember if we've already modded the program counter with the jnz instruction
        already_modded_pc = False

        # Evaluate a "toggle" instruction
        if instruction.code == 'tgl':
            try:
                target_instruction = instructions[pc+registers[params[0]]]
                if len(target_instruction.params) == 1:
                    target_instruction.code = 'dec' if target_instruction.code == 'inc' else 'inc'
                else:
                    target_instruction.code = 'cpy' if target_instruction.code == 'jnz' else 'jnz'
            except IndexError:
                pass

        # Evaluate a "jump if not zero" instruction
        elif instruction.code == 'jnz':
            # Determine the value to check if zero. It's either an integer, or a register reference
            val = params[0]
            if val in registers_list:
                val = registers[val]
            else:
                val = int(val)

            # If the value is not zero, modify the PC by the value of the second parameter.
            if val != 0:
                val2 = params[1]
                if val2 in registers_list:
                    val2 = registers[val2]
                else:
                    val2 = int(val2)

                pc += val2
                already_modded_pc = True

        # Evaluate a "increment" instruction
        elif instruction.code == 'inc':
            registers[params[0]] += 1

        # Evaluate a "decrement" instruction
        elif instruction.code == 'dec':
            registers[params[0]] -= 1

        # Evaluate a "copy" instruction
        elif instruction.code == 'cpy':
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

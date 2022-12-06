from dataclasses import dataclass
from typing import List, Union

#---------------------------------------------------------------------------------------------------

@dataclass
class AssemblyInstruction:
    code: str
    params: List[Union[str, int]]

    @staticmethod
    def from_line(line: str):
        pieces = line.split(' ')
        return AssemblyInstruction(code=pieces[0], params=pieces[1:])


def _deduce_value(val, registers):
    # Determine referenced value. It's either an integer literal, or a register reference.
    try:
        val = int(val)
    except ValueError:
        val = registers[val]
    return val


def evaluate_assembly(registers, instructions):
    """ Evaluates a set of assembly instructions against a set of register values, and returns
    the register values when the instructions terminate. """

    # Init the program counter (pointer to instruction) to 0
    pc = 0

    most_recently_played_freq = None
    recovered_frequency = None

    # While the PC is still pointing to a valid instruction...
    while pc < len(instructions):
        instruction = instructions[pc]
        params = instruction.params

        # Remember if we've already modded the program counter with the jgz instruction
        already_modded_pc = False

        # Evaluate a "sound" instruction
        if instruction.code == 'snd':
            most_recently_played_freq = _deduce_value(params[0], registers)

        # Evaluate a "set" instruction
        elif instruction.code == 'set':
            registers[params[0]] = _deduce_value(params[1], registers)

        # Evaluate an "add" instruction
        elif instruction.code == 'add':
            registers[params[0]] += _deduce_value(params[1], registers)

        # Evaluate a "multiply" instruction
        elif instruction.code == 'mul':
            registers[params[0]] *= _deduce_value(params[1], registers)

        # Evaluate a "modulus" instruction
        elif instruction.code == 'mod':
            registers[params[0]] = registers[params[0]] % _deduce_value(params[1], registers)

        # Evaluate a "recover" instruction
        elif instruction.code == 'rcv':
            if _deduce_value(params[0], registers) != 0:
                recovered_frequency = most_recently_played_freq

        # Evaluate a "jump-greater-than-zero" instruction
        elif instruction.code == 'jgz':
            if _deduce_value(params[0], registers) > 0:
                pc += _deduce_value(params[1], registers)
                already_modded_pc = True

        else:
            raise ValueError(f'WTF is {instruction.code}')

        # If we haven't already modified the PC with a jgz instruction, increment the PC.
        if not already_modded_pc:
            pc += 1

        yield recovered_frequency


def evaluate_assembly_v2(registers, instructions, input_buffer, output_buffer):
    """ Evaluates a set of assembly instructions against a set of register values, and returns
    the register values when the instructions terminate. """

    # Init the program counter (pointer to instruction) to 0
    pc = 0

    waiting_for_rcv = False

    # While the PC is still pointing to a valid instruction...
    while pc < len(instructions):
        instruction = instructions[pc]
        params = instruction.params

        # Remember if we've already modded the program counter with the jgz instruction
        already_modded_pc = False

        # Remember if we need to wait because we're in a receive command and there's
        # nothing in the input queue
        waiting_for_rcv = False

        # Evaluate a "send" instruction
        if instruction.code == 'snd':
            output_buffer.append(_deduce_value(params[0], registers))

        # Evaluate a "set" instruction
        elif instruction.code == 'set':
            registers[params[0]] = _deduce_value(params[1], registers)

        # Evaluate an "add" instruction
        elif instruction.code == 'add':
            registers[params[0]] += _deduce_value(params[1], registers)

        # Evaluate a "multiply" instruction
        elif instruction.code == 'mul':
            registers[params[0]] *= _deduce_value(params[1], registers)

        # Evaluate a "modulus" instruction
        elif instruction.code == 'mod':
            registers[params[0]] = registers[params[0]] % _deduce_value(params[1], registers)

        # Evaluate a "receive" instruction
        elif instruction.code == 'rcv':
            if not input_buffer:
                waiting_for_rcv = True
            else:
                registers[params[0]] = input_buffer.pop(0)

        # Evaluate a "jump-greater-than-zero" instruction
        elif instruction.code == 'jgz':
            if _deduce_value(params[0], registers) > 0:
                pc += _deduce_value(params[1], registers)
                already_modded_pc = True

        else:
            raise ValueError(f'WTF is {instruction.code}')

        # If we haven't already modified the PC with a jgz instruction, and we're not waiting on
        # a receive, increment the PC.
        if not already_modded_pc and not waiting_for_rcv:
            pc += 1

        yield waiting_for_rcv


PCS_OF_INTEREST_AND_DESC = {
    0: 'PC 0 -- Beginning',
    8: 'PC 8 -- Start of loop if G != 0, set F = 1',
    10: 'PC 10 -- Start of loop if G != 0, set E = 2',
    11: 'PC 11 -- Start of loop if G != 0, set G = D',
    14: 'PC 14 -- Set F = 0 if G == 0',
    19: 'PC 19 -- Jump to PC 11 if G != 0',
    23: 'PC 23 -- Jump to PC 10 if G != 0',
    24: 'PC 24 -- Set H = H-1 if F == 0',
    28: 'PC 28 -- End if G == 0, end, else B = B - 17 then jump to PC 8'
}

"""
Notes and musings:

After PC 11 executes every loop:
    - a is always 1
    - b is always 105700
    - c is always 122700
    - d is always 2
    - e counts up by 1, every OTHER loop (skipping to 64, 64, 65, 65, 66, 66)
    - f is always 1
    - g waffles between 2, and counting up (2, -105634, 2, -105633, 2, -105632)
    
    e goes up to 105700 (to match b?) then resets to 0? confirm, I stopped it at e = 3
"""


def evaluate_assembly_v3(registers, instructions, print_debug=False, limit=None):
    """ Evaluates a set of assembly instructions against a set of register values, and returns
    the register values when the instructions terminate. """
    
    total_count = 0
    
    def _debug():
        if not print_debug:
            return
        print('\n')
        print(f'a = {registers["a"]}')
        print(f'b = {registers["b"]}')
        print(f'c = {registers["c"]}')
        print(f'd = {registers["d"]}')
        print(f'e = {registers["e"]}')
        print(f'f = {registers["f"]}')
        print(f'g = {registers["g"]}')
        print(f'h = {registers["h"]}')

    # Init the program counter (pointer to instruction) to 0
    pc = 0
    
    mul_count = 0
    
    pc_11_count = 0
    
    # While the PC is still pointing to a valid instruction...
    while pc < len(instructions):
        total_count += 1
        # if registers['h'] < 0:
        #     print(f'H finally went negative after {total_count}')
        if limit is not None and total_count == limit:
            return

        instruction = instructions[pc]
        params = instruction.params

        # Remember if we've already modded the program counter with the jgz instruction
        already_modded_pc = False

        # Evaluate a "set" instruction
        if instruction.code == 'set':
            registers[params[0]] = _deduce_value(params[1], registers)

        # Evaluate a "multiply" instruction
        elif instruction.code == 'mul':
            mul_count += 1
            registers[params[0]] *= _deduce_value(params[1], registers)

        # Evaluate a "sub" instruction
        elif instruction.code == 'sub':
            registers[params[0]] -= _deduce_value(params[1], registers)

        # Evaluate a "jump-not-zero" instruction
        elif instruction.code == 'jnz':
            if _deduce_value(params[0], registers) != 0:
                pc += _deduce_value(params[1], registers)
                already_modded_pc = True

        else:
            raise ValueError(f'WTF is {instruction.code}')

        if print_debug and pc in PCS_OF_INTEREST_AND_DESC.keys():
            print('\n------------\n')
            if pc == 11:
                pc_11_count += 1
                print(f'e+g = {registers["e"] + registers["g"]}')
            # print(PCS_OF_INTEREST_AND_DESC[pc])
                _debug()
                if pc_11_count == 5:
                    return

        # If we haven't already modified the PC with a jnz instruction
        if not already_modded_pc:
            pc += 1

        yield mul_count
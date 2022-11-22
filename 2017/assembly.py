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

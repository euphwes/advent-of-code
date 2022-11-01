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


def _optimize(instructions):
    """ Optimize the Assembunny instructions by identifying addition loops which
    effectively perform multiplication and replacing with multiplication instructions.

    Ex:
    cpy b c
    inc a
    dec c
    jnz c -2
    dec d
    jnz d -5

    effectively do this:
    a = a + (b * d)
    c = 0
    d = 0
    """

    for i, instruction in enumerate(instructions):
        if instruction.code != 'cpy' or i + 5 >= len(instructions):
            continue

        ordered_next_instrs = ['inc', 'dec', 'jnz', 'dec', 'jnz']
        upcoming_instructions_correct_type = True

        # Peek ahead to the upcoming 5 instructions and make sure they're all
        # the correct type to potentially be a multiplication operation.
        for j in range(5):
            if instructions[i+j+1].code != ordered_next_instrs[j]:
                upcoming_instructions_correct_type = False
                break

        if not upcoming_instructions_correct_type:
            continue

        # In the initial `cpy` command, the first argument is the first multiplicand
        # and the second argument is the register that's the "holding cell" which is depleted and
        # added into the target register.
        multiplicand_1 = instruction.params[0]  # b
        holding_cell = instruction.params[1]    # c

        # In the next instruction, the argument is the register that holds the multiplication result
        next_instr = instructions[i+1]
        resulting_cell = next_instr.params[0]   # a

        # If the following `dec` instruction's argument is not the holding cell register, this set
        # of instructions doesn't match the multiplication pattern.
        next_instr = instructions[i+2]
        if next_instr.params[0] != holding_cell:
            continue

        # If the following `jnz` instruction's argument is not the holding cell register, this set
        # of instructions doesn't match the multiplication pattern.
        next_instr = instructions[i+3]
        if next_instr.params[0] != holding_cell:
            continue

        # In the next instruction, the argument is the second multiplcand.
        next_instr = instructions[i+4]
        multiplicand_2 = next_instr.params[0]  # d

        # If the following `jnz` instruction's argument is not the second multiplcand, this set
        # of instructions doesn't match the multiplication pattern.
        next_instr = instructions[i+5]
        if next_instr.params[0] != multiplicand_2:
            continue

        # Extract the portions of the Assembunny instructions which precede and follow the portion
        # to be optimized.
        before_mul = instructions[:i]
        after_mul = instructions[i+6:]

        # Build the multiplication instruction, and also write 0 to the holding cell and
        # multiplicand 2 register since that's what the loop does. The total number of instructions
        # should be the same (so we don't mess up `jnz` instructions which index by count).
        mul_instructions = list(map(AssembunnyInstruction.from_line, [
            f'mul {resulting_cell} {multiplicand_1} {multiplicand_2}',
            f'cpy 0 {holding_cell}',
            f'cpy 0 {multiplicand_2}',
            'nop',
            'nop',
            'nop',
        ]))

        # Update the instructions, replacing the addition loop with optimized multiplication
        instructions = before_mul + mul_instructions + after_mul

    return instructions


def evaluate_assembunny(registers, instructions):
    """ Evaluates a set of assembunny instructions against a set of register values, and returns
    the register values when the instructions terminate. """

    instructions = _optimize(instructions)

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
                instructions = _optimize(instructions)
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
            if src in registers_list:
                src = registers[src]
            else:
                src = int(src)

            # Update the destination register with the source value.
            registers[dst] = src

        # Evaluate a "multiply" instruction
        elif instruction.code == 'mul':
            target_cell = instruction.params[0]
            m1, m2 = instruction.params[1], instruction.params[2]

            if m1 in registers_list:
                m1 = registers[m1]
            else:
                m1 = int(m1)

            if m2 in registers_list:
                m2 = registers[m2]
            else:
                m2 = int(m2)

            registers[target_cell] += (m1*m2)

        # Evaluate a "no-op" instruction
        elif instruction.code == 'nop':
            pass

        else:
            raise ValueError(f'WTF is {instruction.code}')

        # If we haven't already modified the PC with a jnz instruction, increment the PC.
        if not already_modded_pc:
            pc += 1

    # Done evaluating the instructions, return the register values.
    return registers

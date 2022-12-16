from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 23
YEAR = 2015

PART_ONE_DESCRIPTION = "value of register b"
PART_ONE_ANSWER = 255

PART_TWO_DESCRIPTION = "value of register b if register a starts with 1"
PART_TWO_ANSWER = 334


class AssemblyInterpreter:

    REGISTER_A = "a"
    REGISTER_B = "b"

    INSTRUCTION_HLF = "hlf"
    INSTRUCTION_TPL = "tpl"
    INSTRUCTION_INC = "inc"
    INSTRUCTION_JMP = "jmp"
    INSTRUCTION_JIE = "jie"
    INSTRUCTION_JIO = "jio"

    def __init__(self):
        self.register_a = 0
        self.register_b = 0
        self.instruction_ptr = 0

        self.instructions_map = {
            AssemblyInterpreter.INSTRUCTION_HLF: self.enact_hlf,
            AssemblyInterpreter.INSTRUCTION_TPL: self.enact_tpl,
            AssemblyInterpreter.INSTRUCTION_INC: self.enact_inc,
            AssemblyInterpreter.INSTRUCTION_JMP: self.enact_jmp,
            AssemblyInterpreter.INSTRUCTION_JIE: self.enact_jie,
            AssemblyInterpreter.INSTRUCTION_JIO: self.enact_jio,
        }

    def execute_program(self, program):
        self.program = program

        while True:
            try:
                instruction = self.program[self.instruction_ptr]
                self.execute_instruction(instruction)
            except IndexError:
                return

    def execute_instruction(self, instruction):
        instruction_parts = [
            x.replace(",", "").replace("\n", "") for x in instruction.split(" ")
        ]
        operation, args = instruction_parts[0], instruction_parts[1:]

        self.instructions_map[operation](*args)

    def enact_hlf(self, target_register):
        """Enact a 'half' instruction by halving the value in the target register, then advancing
        the instruction pointer to the next instruction."""

        if target_register == AssemblyInterpreter.REGISTER_A:
            self.register_a = self.register_a / 2
        else:
            self.register_b = self.register_b / 2

        self.instruction_ptr += 1

    def enact_tpl(self, target_register):
        """Enact a 'triple' instruction by tripling the value in the target register, then
        advancing the instruction pointer to the next instruction."""

        if target_register == AssemblyInterpreter.REGISTER_A:
            self.register_a = self.register_a * 3
        else:
            self.register_b = self.register_b * 3

        self.instruction_ptr += 1

    def enact_inc(self, target_register):
        """Enact an 'increment' instruction by incrementing the value in the target register, then
        advancing the instruction pointer to the next instruction."""

        if target_register == AssemblyInterpreter.REGISTER_A:
            self.register_a += 1
        else:
            self.register_b += 1

        self.instruction_ptr += 1

    def enact_jmp(self, offset):
        """Enact a 'jump' instruction by advancing the instruction pointer to the instruction
        specified by the supplied offset."""

        self.instruction_ptr += int(offset)

    def enact_jie(self, target_register, offset):
        """Enact a 'jump if event' instruction by checking if the target register holds an even
        value, and advancing the instruction pointer to the instruction specified by the supplied
        offset if true."""

        if target_register == AssemblyInterpreter.REGISTER_A:
            if self.register_a % 2 == 0:
                self.instruction_ptr += int(offset)
            else:
                self.instruction_ptr += 1
        else:
            if self.register_b % 2 == 0:
                self.instruction_ptr += int(offset)
            else:
                self.instruction_ptr += 1

    def enact_jio(self, target_register, offset):
        """Enact a 'jump if one' instruction by checking if the target register holds a value of 1,
                and advancing the instruction pointer to the instruction specified by the supplied offset
        if true."""

        if target_register == AssemblyInterpreter.REGISTER_A:
            if self.register_a == 1:
                self.instruction_ptr += int(offset)
            else:
                self.instruction_ptr += 1
        else:
            if self.register_b == 1:
                self.instruction_ptr += int(offset)
            else:
                self.instruction_ptr += 1


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(program):
    computer = AssemblyInterpreter()
    computer.execute_program(program)

    return computer.register_b


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(program):
    computer = AssemblyInterpreter()
    computer.register_a = 1

    computer.execute_program(program)

    return computer.register_b


# ----------------------------------------------------------------------------------------------


def run(input_file):

    program = get_input(input_file)

    part_one(program)
    part_two(program)

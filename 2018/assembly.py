from dataclasses import dataclass
from typing import Callable, Dict, List

from util.input import safe_eval

# ----------------------------------------------------------------------------------------------


@dataclass
class AssemblyInstruction:
    """Represents an instruction in a program. Contains an opcode and 3 parameters."""

    code: int
    params: List[int]

    @staticmethod
    def from_line(line: str):
        """Returns an AssemblyInstruction as parsed from a line of the input."""

        pieces = [int(n) for n in line.split(" ")]
        return AssemblyInstruction(code=pieces[0], params=pieces[1:])


@dataclass
class CompleteAssemblyInstruction:
    """Represents an instruction in a program. Contains an operation and 3 parameters."""

    operation_txt: str
    operation: Callable
    params: List[int]

    @staticmethod
    def from_line(line: str):
        """Returns an CompleteAssemblyInstruction as parsed from a line of the input."""

        pieces = line.split(" ")
        params = [int(n) for n in pieces[1:]]

        operation = {
            "addr": _addr,
            "addi": _addi,
            "mulr": _mulr,
            "muli": _muli,
            "banr": _banr,
            "bani": _bani,
            "borr": _borr,
            "bori": _bori,
            "setr": _setr,
            "seti": _seti,
            "gtir": _gtir,
            "gtri": _gtri,
            "gtrr": _gtrr,
            "eqir": _eqir,
            "eqri": _eqri,
            "eqrr": _eqrr,
        }[pieces[0]]

        return CompleteAssemblyInstruction(
            operation_txt=pieces[0], operation=operation, params=params
        )

    def execute(self, registers):
        return self.operation(self.params, registers)

    def __str__(self):
        return f"{self.operation_txt} {' '.join([str(x) for x in self.params])}"


class AssemblyComputer:
    def __init__(self, raw_program):
        self.ip = 0
        self.ip_register = None

        # If the first line in a program is a declaration binding the IP
        # to a register, remember which register. Ex: #ip 4
        if raw_program[0].startswith("#"):
            ip_bind_line = raw_program.pop(0)
            self.ip_register = int(ip_bind_line.split(" ")[-1])

        self.program = [
            CompleteAssemblyInstruction.from_line(line) for line in raw_program
        ]
        self.program_size = len(self.program)

        self.registers = {n: 0 for n in range(6)}

    def run(self):
        while True:
            if self.ip >= self.program_size:
                return

            if self.ip_register is not None:
                self.registers[self.ip_register] = self.ip

            # print(f"\n[{' '.join([str(x) for x in self.registers.values()])}]")
            instruction = self.program[self.ip]
            # print(f"{self.ip} {instruction}")
            self.registers = instruction.execute(self.registers)
            # print(f"[{' '.join([str(x) for x in self.registers.values()])}]")

            if self.ip_register is not None:
                self.ip = self.registers[self.ip_register] + 1


class StepwiseAssemblyComputer:
    def __init__(self, raw_program):
        self.ip = 0
        self.ip_register = None

        # If the first line in a program is a declaration binding the IP
        # to a register, remember which register. Ex: #ip 4
        if raw_program[0].startswith("#"):
            ip_bind_line = raw_program.pop(0)
            self.ip_register = int(ip_bind_line.split(" ")[-1])

        self.program = [
            CompleteAssemblyInstruction.from_line(line) for line in raw_program
        ]
        self.program_size = len(self.program)

        self.registers = {n: 0 for n in range(6)}

    def run(self):
        c = 0
        while True:
            if self.ip >= self.program_size:
                return

            c += 1
            yield c, self.ip, self.registers

            if self.ip_register is not None:
                self.registers[self.ip_register] = self.ip

            # print(f"\n[{' '.join([str(x) for x in self.registers.values()])}]")
            instruction = self.program[self.ip]
            # print(f"{self.ip} {instruction}")
            self.registers = instruction.execute(self.registers)
            # print(f"[{' '.join([str(x) for x in self.registers.values()])}]")

            if self.ip_register is not None:
                self.ip = self.registers[self.ip_register] + 1


@dataclass
class AssemblyTestCase:
    """Represents a test case for an assembly instruction.

    Contains a set of registers values before and after the instruction completes,
    as well as the instruction itself."""

    registers_before: Dict[int, int]
    registers_after: Dict[int, int]
    instruction: AssemblyInstruction

    @staticmethod
    def from_lines(before_line: str, instruction_line: str, after_line: str):
        """Returns an AssemblyTestCase as parsed from 3 consecutive lines of the input."""

        # Evaluate the portion of these lines which are just a list of integers, and
        # store it as a dictionary of register values.

        before_list = safe_eval(before_line.replace("Before:", ""))
        assert isinstance(before_list, list)

        after_list = safe_eval(after_line.replace("After:", ""))
        assert isinstance(after_list, list)

        registers_before = {i: n for i, n in enumerate(before_list)}
        registers_after = {i: n for i, n in enumerate(after_list)}

        return AssemblyTestCase(
            registers_before=registers_before,
            registers_after=registers_after,
            instruction=AssemblyInstruction.from_line(instruction_line),
        )

    def does_work_for_function(self, fn):
        """For a given operator function, return if this test case "works"; that is,
        if the provided parameters and input register values return the expected output
        register values."""

        before_copy = {a: b for a, b in self.registers_before.items()}
        return fn(self.instruction.params, before_copy) == self.registers_after


def _addr(params, registers):
    val1 = registers[params[0]]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = val1 + val2
    return registers


def _addi(params, registers):
    val1 = registers[params[0]]
    val2 = params[1]
    dest = params[2]
    registers[dest] = val1 + val2
    return registers


def _mulr(params, registers):
    val1 = registers[params[0]]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = val1 * val2
    return registers


def _muli(params, registers):
    val1 = registers[params[0]]
    val2 = params[1]
    dest = params[2]
    registers[dest] = val1 * val2
    return registers


def _banr(params, registers):
    val1 = registers[params[0]]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = val1 & val2
    return registers


def _bani(params, registers):
    val1 = registers[params[0]]
    val2 = params[1]
    dest = params[2]
    registers[dest] = val1 & val2
    return registers


def _borr(params, registers):
    val1 = registers[params[0]]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = val1 | val2
    return registers


def _bori(params, registers):
    val1 = registers[params[0]]
    val2 = params[1]
    dest = params[2]
    registers[dest] = val1 | val2
    return registers


def _setr(params, registers):
    val1 = registers[params[0]]
    dest = params[2]
    registers[dest] = val1
    return registers


def _seti(params, registers):
    val1 = params[0]
    dest = params[2]
    registers[dest] = val1
    return registers


def _gtir(params, registers):
    val1 = params[0]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = 1 if val1 > val2 else 0
    return registers


def _gtri(params, registers):
    val1 = registers[params[0]]
    val2 = params[1]
    dest = params[2]
    registers[dest] = 1 if val1 > val2 else 0
    return registers


def _gtrr(params, registers):
    val1 = registers[params[0]]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = 1 if val1 > val2 else 0
    return registers


def _eqir(params, registers):
    val1 = params[0]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = 1 if val1 == val2 else 0
    return registers


def _eqri(params, registers):
    val1 = registers[params[0]]
    val2 = params[1]
    dest = params[2]
    registers[dest] = 1 if val1 == val2 else 0
    return registers


def _eqrr(params, registers):
    val1 = registers[params[0]]
    val2 = registers[params[1]]
    dest = params[2]
    registers[dest] = 1 if val1 == val2 else 0
    return registers


ALL_OPERATORS = [
    _addr,
    _addi,
    _mulr,
    _muli,
    _banr,
    _bani,
    _borr,
    _bori,
    _setr,
    _seti,
    _gtir,
    _gtri,
    _gtrr,
    _eqir,
    _eqri,
    _eqrr,
]

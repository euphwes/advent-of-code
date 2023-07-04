from dataclasses import dataclass
from typing import Dict, List

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

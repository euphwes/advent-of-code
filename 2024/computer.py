from types import NoneType


class Computer:
    """A computer than can execute arbitrary pseudo-assembly programs.

    The language spec for AoC 2024 is defined: https://adventofcode.com/2024/day/17
    """

    OPCODE_ADV = 0  # 0, <combo operand>
    OPCODE_BXL = 1  # 1, <literal operand>
    OPCODE_BST = 2  # 2, <combo operand>
    OPCODE_JNZ = 3  # 3, <literal operand>
    OPCODE_BXC = 4  # 4, <operand ignored>
    OPCODE_OUT = 5  # 5, <combo operand>
    OPCODE_BDV = 6  # 6, <combo operand>
    OPCODE_CDV = 7  # 7, <combo operand>

    def __init__(
        self,
        program: list[int],
        initial_registers: dict[str, int] | None = None,
    ) -> None:
        """Initialize an Intcode computer.

        Sets the instruction pointer to address 0, and establishes some maps defining which
        action to take for any given opcode.
        """
        self.instruction_ptr = 0
        self.program = program

        self.registers = (
            initial_registers.copy()
            if initial_registers is not None
            else {
                "A": 0,
                "B": 0,
                "C": 0,
            }
        )

        self.output: list[int] = []

        self.opcode_map = {
            Computer.OPCODE_ADV: self._enact_adv,
            Computer.OPCODE_BXL: self._enact_bxl,
            Computer.OPCODE_BST: self._enact_bst,
            Computer.OPCODE_JNZ: self._enact_jnz,
            Computer.OPCODE_BXC: self._enact_bxc,
            Computer.OPCODE_OUT: self._enact_out,
            Computer.OPCODE_BDV: self._enact_bdv,
            Computer.OPCODE_CDV: self._enact_cdv,
        }

    def execute(self) -> list[int]:
        """Execute the provided program with the specified input."""

        while self.instruction_ptr < len(self.program):
            # Retrieve the next opcode and param modes, and execute that instruction.
            opcode, param_value = self._get_opcode_and_operand()

            prior_ip = self.instruction_ptr
            self.opcode_map[opcode](param_value)
            later_ip = self.instruction_ptr

            # If the instruction just executed modified the instruction pointer directly,
            # skip advancing the instruction pointer
            if opcode != 3 or prior_ip == later_ip:  # noqa: PLR2004
                self.instruction_ptr += 2

        return self.output

    def _get_opcode_and_operand(self) -> tuple[int, int | None]:
        """Parse the opcode and operand based on the instruction pointer's current value."""

        opcode = self.program[self.instruction_ptr]
        param = self.program[self.instruction_ptr + 1]

        # Opcode 4 ignores the operand
        if opcode == 4:  # noqa: PLR2004
            return opcode, None

        # Operands to opcodes 1, 3 are literal operands
        if opcode in {1, 3}:
            return opcode, param

        # Operands to opcodes 0, 2, 5, 6, 7 are combo operands

        # Combo operands 0 through 3 represent literal values 0 through 3.
        if param in {0, 1, 2, 3}:
            return opcode, param

        # Combo operand 4 represents the value of register A.
        # Combo operand 5 represents the value of register B.
        # Combo operand 6 represents the value of register C.
        return opcode, {
            4: self.registers["A"],
            5: self.registers["B"],
            6: self.registers["C"],
        }[param]

    def _enact_adv(self, operand: int) -> None:
        self.registers["A"] = self.registers["A"] // (2**operand)

    def _enact_bdv(self, operand: int) -> None:
        self.registers["B"] = self.registers["A"] // (2**operand)

    def _enact_cdv(self, operand: int) -> None:
        self.registers["C"] = self.registers["A"] // (2**operand)

    def _enact_bxl(self, operand: int) -> None:
        self.registers["B"] = self.registers["B"] ^ operand

    def _enact_bst(self, operand: int) -> None:
        self.registers["B"] = operand % 8

    def _enact_out(self, operand: int) -> None:
        self.output.append(operand % 8)

    def _enact_jnz(self, operand: int) -> None:
        if self.registers["A"] != 0:
            self.instruction_ptr = operand

    def _enact_bxc(self, _: NoneType) -> None:
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

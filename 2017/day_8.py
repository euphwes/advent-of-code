from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

#---------------------------------------------------------------------------------------------------

@dataclass
class Operation:
    target_register: str
    operator: Callable[[int, int], int]
    operand: int

    def apply(self, registers):
        target_value = registers[self.target_register]
        new_value = self.operator(target_value, self.operand)
        registers[self.target_register] = new_value
        return registers


@dataclass
class Condition:
    target_register: str
    operator: Callable[[int, int], bool]
    operand: int

    def matches(self, registers):
        target_value = registers[self.target_register]
        return self.operator(target_value, self.operand)


@dataclass
class Instruction:
    operation: Operation
    condition: Condition

    @staticmethod
    def parse(raw_instruction):
        # Split raw instruction into left and right sides (operation and condition)
        operation_side, condition_side = raw_instruction.split(' if ')

        # Split the condition side and build Condition
        condition_register, condition_operator, condition_operand = condition_side.split()
        condition = Condition(
            target_register=condition_register,
            operand=int(condition_operand),
            operator={
                '>': lambda x, y: x > y,
                '<': lambda x, y: x < y,
                '>=': lambda x, y: x >= y,
                '<=': lambda x, y: x <= y,
                '==': lambda x, y: x == y,
                '!=': lambda x, y: x != y,
            }[condition_operator]
        )

        # Split the operation side and build Operation
        operation_register, operation_operator, operation_operand = operation_side.split()
        operation = Operation(
            target_register=operation_register,
            operand=int(operation_operand),
            operator={
                'inc': lambda x, y: x + y,
                'dec': lambda x, y: x - y,
            }[operation_operator]
        )

        return Instruction(operation=operation, condition=condition)


    def apply(self, registers):
        if self.condition.matches(registers):
            return self.operation.apply(registers)
        return registers



@aoc_output_formatter(2017, 8, 1, 'value of the largest register')
def part_one(raw_instructions):
    registers = defaultdict(int)
    for raw_instruction in raw_instructions:
        registers = Instruction.parse(raw_instruction).apply(registers)
    return max(registers.values())


@aoc_output_formatter(2017, 8, 2, 'largest value a register ever held')
def part_two(raw_instructions):
    stepwise_maxes = list()
    registers = defaultdict(int)
    for raw_instruction in raw_instructions:
        registers = Instruction.parse(raw_instruction).apply(registers)
        stepwise_maxes.append(max(registers.values()))
    return max(stepwise_maxes)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw_instructions = get_input(input_file)

    part_one(raw_instructions)
    part_two(raw_instructions)

from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict

#---------------------------------------------------------------------------------------------------

TuringMachineState = Enum('TuringMachineState', {c: c for c in 'ABCDEF'})


@dataclass
class Operation:
    new_value: int
    cursor_change: int
    next_state: TuringMachineState


# Mostly just because it helped me figure out the structures I'm building when parsing the input...

# A map that describes which Operation (new tape value, which way the cursor moves, and next state)
# depending on the current value of the tape at the cursor.
CurrentValueOperationMap = Dict[int, Operation]

# A map that describes the CurrentValueOperationMap to reference depending on the current state
# of the Turing machine.
StateOperationMap = Dict[TuringMachineState, CurrentValueOperationMap]


class TuringMachine:
    """ Defines a Turing machine in a specific state and an infinite tape. """
 
    def __init__(self, starting_state: TuringMachineState):
        self.tape = defaultdict(int)
        self.cursor = 0
        self.state = starting_state

    def run(self, step_count: int, state_op_map: StateOperationMap):
        """ Run for `step_count` steps using the rules defined in state_op_map. """

        for _ in range(step_count):
            curr_value = self.tape[self.cursor]
            operation = state_op_map[self.state][curr_value]

            self.tape[self.cursor] = operation.new_value
            self.cursor += operation.cursor_change
            self.state = operation.next_state

    def get_checksum(self):
        """ Returns the machine's checksum which is the sum of all 1-values on the tape. """

        return sum(self.tape.values())


def _parse_turing_machine_instructions(instructions):
    """ Parse starting state, step count, and a StateOperationMap comprised of
    CurrentValueOperationMaps from the problem input. """

    starting_state = instructions.pop(0).replace('Begin in state ', '').replace('.', '')
    starting_state = TuringMachineState[starting_state]

    step_count = instructions.pop(0).replace('Perform a diagnostic checksum after ', '')
    step_count = step_count.replace(' steps.', '')
    step_count = int(step_count)

    # Blank line
    instructions.pop(0)

    state_op_map = dict()

    while instructions:
        # Peel off 10 lines at a time, which comprise all the info needed to build a
        # CurrentValueOperationMap for the specified TuringMachineState
        current, instructions = instructions[:10], instructions[10:]
        curr_state = TuringMachineState[current[0].replace('In state ','')[0]]

        # operation-if-0
        new_value = int(current[2][-2])
        cursor_change = 1 if current[3][-3] == 'h' else -1  # right has 'h', left does not
        next_state = TuringMachineState[current[4][-2]]

        op_if_0 = Operation(new_value=new_value, cursor_change=cursor_change, next_state=next_state)

        # operation-if-1
        new_value = int(current[6][-2])
        cursor_change = 1 if current[7][-3] == 'h' else -1  # right has 'h', left does not
        next_state = TuringMachineState[current[8][-2]]

        op_if_1 = Operation(new_value=new_value, cursor_change=cursor_change, next_state=next_state)

        value_op_map = { 0: op_if_0, 1: op_if_1 }
        state_op_map[curr_state] = value_op_map

    return starting_state, step_count, state_op_map


@aoc_output_formatter(2017, 25, 1, 'Turing machine checksum', assert_answer=3554)
def part_one(instructions):
    starting_state, step_count, op_map = _parse_turing_machine_instructions(instructions)

    computer = TuringMachine(starting_state)
    computer.run(step_count, op_map)

    return computer.get_checksum()

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = get_input(input_file)
    part_one(instructions)

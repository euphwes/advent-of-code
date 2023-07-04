from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembly import ALL_OPERATORS, AssemblyInstruction, AssemblyTestCase

DAY = 16
YEAR = 2018

PART_ONE_DESCRIPTION = "Number of samples that behave like 3 or more opcodes"
PART_ONE_ANSWER = 570

PART_TWO_DESCRIPTION = "Value in register 0 after the program completes"
PART_TWO_ANSWER = 503


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(test_cases):
    test_cases_matching_three_ops = 0

    # For each test case...
    for case in test_cases:
        # ... count the number of operators which satisfy this test case.
        # That is, the given instruction parameters and the operator being tested,
        # turn the starting state of registers into the specified end state.
        matching_ops = 0
        for op in ALL_OPERATORS:
            if case.does_work_for_function(op):
                matching_ops += 1

        # If this test case worked for at least 3 operators, count it.
        if matching_ops >= 3:
            test_cases_matching_three_ops += 1

    return test_cases_matching_three_ops


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(test_cases, instructions):
    # Maintain a dictionary mapping integer opcode to the operator it corresponds to.
    # Also track which operators are still unmapped.
    opcode_mappings = dict()
    unmapped_operators = [x for x in ALL_OPERATORS]

    while unmapped_operators:
        # For each test case that has an instruction opcode that hasn't been mapped...
        for case in test_cases:
            if case.instruction.code in opcode_mappings:
                continue

            # ... identify which remaining unmapped operators apply to this test case.
            matching_ops = set()
            for op in unmapped_operators:
                if case.does_work_for_function(op):
                    matching_ops.add(op)

            # If only one remaining operator works for this case, then we can map
            # that operator to the instruction's opcode, and remove that operator
            # from the unmapped operators (because we no longer need to test it).
            if len(matching_ops) == 1:
                matching_op = list(matching_ops)[0]
                opcode_mappings[case.instruction.code] = matching_op
                unmapped_operators.remove(matching_op)

    # Now that we know which opcode corresponds to which operators, start all the registers
    # at 0 and then run each instruction sequentially.
    registers = {0: 1, 1: 0, 2: 0, 3: 0}
    for inst in instructions:
        registers = opcode_mappings[inst.code](inst.params, registers)

    return registers[0]


# ----------------------------------------------------------------------------------------------


def run(input_file):
    raw_input = get_input(input_file)

    test_cases = []

    # Take 3 lines at a time.
    # The first is the starting state of registers.
    # The second is the assembly instruction.
    # The third is the final state of registers.
    raw_test_info = [x for x in raw_input[:3093] if x]
    while raw_test_info:
        before_line = raw_test_info.pop(0)
        instruction_line = raw_test_info.pop(0)
        after_line = raw_test_info.pop(0)

        test_cases.append(
            AssemblyTestCase.from_lines(
                before_line,
                instruction_line,
                after_line,
            )
        )

    instructions = [AssemblyInstruction.from_line(line) for line in raw_input[3094:]]

    part_one(test_cases)
    part_two(test_cases, instructions)

from collections.abc import Generator
from itertools import permutations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 24
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _parse_wire_values(raw_input: list[str]) -> dict[str, int]:
    blank_ix = raw_input.index("")
    wire_values = {}
    for line in raw_input[:blank_ix]:
        wire, value = line.split(": ")
        wire_values[wire] = int(value)
    return wire_values


def _parse_wire_operations(raw_input: list[str]) -> list[list[str]]:
    blank_ix = raw_input.index("")

    # wire operations are
    # input1, operation, input2, output
    operations = []
    ops_leading_to_x_or_y = []
    other_ops = []

    for line in raw_input[blank_ix + 1 :]:
        inp, outp = line.split(" -> ")
        in1, op, in2 = inp.split(" ")

        in1, in2 = sorted([in1, in2])

        if in1[0] in ("x", "y") or in2[0] in ("x", "y"):
            ops_leading_to_x_or_y.append([in1, op, in2, outp])
        else:
            other_ops.append([in1, op, in2, outp])
        # operations.append([in1, op, in2, outp])

    ops_leading_to_x_or_y.sort(key=lambda x: x[0])
    other_ops.sort(key=lambda x: x[3])
    # other_ops.sort(key=lambda x: x[1])  # sort by operation

    operations.extend(ops_leading_to_x_or_y)
    operations.extend(other_ops)

    return operations


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    wire_values = _parse_wire_values(raw_input)
    wire_operations = _parse_wire_operations(raw_input)

    while wire_operations:
        in1, op, in2, outp = wire_operations.pop(0)
        if in1 in wire_values and in2 in wire_values:
            if op == "AND":
                wire_values[outp] = wire_values[in1] & wire_values[in2]
            elif op == "OR":
                wire_values[outp] = wire_values[in1] | wire_values[in2]
            elif op == "XOR":
                wire_values[outp] = wire_values[in1] ^ wire_values[in2]
            else:
                raise ValueError(f"Unknown operation: {op}")
        else:
            wire_operations.append([in1, op, in2, outp])

    z_wires = sorted([wire for wire in wire_values if wire[0] == "z"], reverse=True)
    return int(
        "".join(str(wire_values[wire]) for wire in z_wires),
        2,
    )


def _swapped_wire_output_possibilities(
    wire_operations: list[list[str]],
) -> Generator[tuple[list[list[str]], list[str]]]:
    all_outputs = [f[3] for f in wire_operations]

    for p1, p2, p3, p4 in permutations(all_outputs, 4):
        wire_ops_copy = wire_operations.copy()
        for f in wire_ops_copy:
            if f[3] == p1:
                f[3] = p2
            elif f[3] == p2:
                f[3] = p1
            elif f[3] == p3:
                f[3] = p4
            elif f[3] == p4:
                f[3] = p3
        yield wire_ops_copy, [p1, p2, p3, p4]


def _solve(
    wire_operations: list[list[str]],
    wire_values: dict[str, int],
) -> int:
    while wire_operations:
        in1, op, in2, outp = wire_operations.pop(0)
        if in1 in wire_values and in2 in wire_values:
            if op == "AND":
                wire_values[outp] = wire_values[in1] & wire_values[in2]
            elif op == "OR":
                wire_values[outp] = wire_values[in1] | wire_values[in2]
            elif op == "XOR":
                wire_values[outp] = wire_values[in1] ^ wire_values[in2]
            else:
                raise ValueError(f"Unknown operation: {op}")
        else:
            wire_operations.append([in1, op, in2, outp])

    z_wires = sorted([wire for wire in wire_values if wire[0] == "z"], reverse=True)
    return int(
        "".join(str(wire_values[wire]) for wire in z_wires),
        2,
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    wire_values = _parse_wire_values(raw_input)
    wire_operations = _parse_wire_operations(raw_input)

    # start a mermaid graph TD output with maxEdges set to 1000
    mermaid_output = "graph TD\n"

    # each element in wire_operations is of the form
    # (input1, operation, input2, output)

    input_wires = sorted(wire_values.keys())
    for wire in input_wires:
        mermaid_output += f"    {wire}({wire})\n"

    # iterate over the connections and build up the mermaid output
    # each input wire is a node, leading to a node for the operation.
    # the operation node leads to the output wire node

    AND_COUNT = 0
    OR_COUNT = 0
    XOR_COUNT = 0

    operator_nodes = []
    z_nodes = []

    for in1, op, in2, outp in wire_operations:
        sop = None
        if op == "AND":
            AND_COUNT += 1
            sop = f"AND{AND_COUNT}" + "{AND}"
            operator_nodes.append(f"AND{AND_COUNT}")
        elif op == "OR":
            OR_COUNT += 1
            sop = f"OR{OR_COUNT}" + "{{OR}}"
            operator_nodes.append(f"OR{OR_COUNT}")
        elif op == "XOR":
            XOR_COUNT += 1
            sop = f"XOR{XOR_COUNT}" + "[XOR]"
            operator_nodes.append(f"XOR{XOR_COUNT}")

        if outp[0] == "z":
            z_nodes.append(outp)

        mermaid_output += f"    {in1}({in1}) --> {sop}\n"
        mermaid_output += f"    {in2}({in2}) --> {sop}\n"
        mermaid_output += f"    {sop} --> {outp}({outp})\n"

    for node in operator_nodes:
        if node.startswith("AND"):
            # red
            mermaid_output += f"    style {node} fill:#f9d0c4\n"
        elif node.startswith("OR"):
            # blue
            mermaid_output += f"    style {node} fill:#c4e4f9\n"
        elif node.startswith("XOR"):
            # green
            mermaid_output += f"    style {node} fill:#c4f9c4\n"

    # write z nodes with heavy stroke, black background and white text
    for node in z_nodes:
        mermaid_output += (
            f"    style {node} fill:#333333,stroke:#333333,stroke-width:2px,color:#ffffff\n"
        )

    # write to file
    with open("day24_adder_trial4.mmd", "w") as f:
        f.write(mermaid_output)

    # manually inspecting the Mermaid graph output,
    # finding discrepancies in the pattern of the adder circuitry
    return "cph,jqn,kwb,qkf,tgr,z12,z16,z24"


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

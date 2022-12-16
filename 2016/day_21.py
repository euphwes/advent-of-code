from enum import Enum

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 21
YEAR = 2016

PART_ONE_DESCRIPTION = "result of scrambling abcdefgh"
PART_ONE_ANSWER = "dgfaehcb"

PART_TWO_DESCRIPTION = "unscrambled version of the scrambled password fbgdceah"
PART_TWO_ANSWER = "fdhgacbe"


class InstructionCode(Enum):
    SWAP_POSITION = "swap_pos"
    SWAP_LETTER = "swap_letter"
    ROTATE_LETTER = "rotate_letter"
    ROTATE_DIRECTION = "rotate_direction"
    REVERSE_POSITIONS = "reverse_positions"
    MOVE = "move"


def _parse_input(lines):
    """Parses the problem input and returns a list of instructions for scrambling the
    passcode."""

    instructions = list()
    for line in lines:
        if "swap position" in line:
            f, b = line.split(" with position ")
            f = int(f.replace("swap position ", ""))
            b = int(b)
            instructions.append([InstructionCode.SWAP_POSITION, f, b])
        elif "swap letter" in line:
            f, b = line.split(" with letter ")
            f = f.replace("swap letter ", "")
            instructions.append([InstructionCode.SWAP_LETTER, f, b])
        elif "rotate based" in line:
            x = line.replace("rotate based on position of letter ", "")
            instructions.append([InstructionCode.ROTATE_LETTER, x])
        elif "rotate" in line:
            parts = line.split(" ")
            instructions.append(
                [InstructionCode.ROTATE_DIRECTION, parts[1], int(parts[2])]
            )
        elif "reverse" in line:
            line = line.replace("reverse positions ", "")
            f, b = line.split(" through ")
            instructions.append([InstructionCode.REVERSE_POSITIONS, int(f), int(b)])
        elif "move" in line:
            line = line.replace("move position ", "")
            f, b = line.split(" to position ")
            instructions.append([InstructionCode.MOVE, int(f), int(b)])

    return instructions


def _swap_position(passcode, args, is_reverse=False):
    """Swaps the letters at indices f and b in the passcode."""

    f, b = args
    passcode = list(passcode)
    temp = passcode[f]
    passcode[f] = passcode[b]
    passcode[b] = temp

    return "".join(passcode)


def _swap_letter(passcode, args, is_reverse=False):
    """Swaps the letters specified in the passcode."""

    (
        f,
        b,
    ) = args
    passcode = passcode.replace(f, "~")
    passcode = passcode.replace(b, f)
    passcode = passcode.replace("~", b)

    return passcode


def _rotate(passcode, dir, n):
    """Rotates the provided passcode in the specified direction by `n`."""

    n = n % len(passcode)

    if dir == "right":
        n *= -1
    return passcode[n:] + passcode[:n]


def _rotate_based_on_letter(passcode, args, is_reverse=False):
    """Rotate the passcode based on the index of the provided letter + 1. If the index was at
    least 4, rotate 1 additional."""

    if is_reverse:
        for n in range(len(passcode)):
            start_candidate = _rotate(passcode, "left", n)
            if (
                _rotate_based_on_letter(start_candidate, args, is_reverse=False)
                == passcode
            ):
                return start_candidate
        raise Exception("Should have found the previous state.")

    i = passcode.index(args[0])
    n = i + 1
    if i >= 4:
        n += 1

    return _rotate(passcode, "right", n)


def _rotate_direction(passcode, args, is_reverse=False):
    """Rotate the passcode the specified direction and amount."""

    dir, n = args

    if is_reverse:
        n *= -1

    return _rotate(passcode, dir, n)


def _reverse_positions(passcode, args, is_reverse=False):
    """Within the passcode, reverse the order of the letters within the range specified."""

    f, b = args
    return passcode[:f] + "".join(reversed(passcode[f : b + 1])) + passcode[b + 1 :]


def _move(passcode, args, is_reverse=False):
    """Moves a character in the passcode from index f to index b."""

    f, b = args
    if is_reverse:
        b, f = f, b

    char = passcode[f]
    passcode = passcode[:f] + passcode[f + 1 :]
    passcode = passcode[:b] + char + passcode[b:]
    return passcode


INSTRUCTION_MAP = {
    InstructionCode.SWAP_POSITION: _swap_position,
    InstructionCode.SWAP_LETTER: _swap_letter,
    InstructionCode.ROTATE_LETTER: _rotate_based_on_letter,
    InstructionCode.ROTATE_DIRECTION: _rotate_direction,
    InstructionCode.REVERSE_POSITIONS: _reverse_positions,
    InstructionCode.MOVE: _move,
}


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions):
    passcode = "abcdefgh"
    for instr in instructions:
        code = instr[0]
        args = instr[1:]
        passcode = INSTRUCTION_MAP[code](passcode, args, is_reverse=False)
    return passcode


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(instructions):
    passcode = "fbgdceah"
    for instr in instructions[::-1]:
        code = instr[0]
        args = instr[1:]
        passcode = INSTRUCTION_MAP[code](passcode, args, is_reverse=True)
    return passcode


# ----------------------------------------------------------------------------------------------


def run(input_file):
    instructions = _parse_input(get_input(input_file))

    part_one(instructions)
    part_two(instructions)

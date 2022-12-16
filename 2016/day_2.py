from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 2
YEAR = 2016

PART_ONE_DESCRIPTION = "bathroom code"
PART_ONE_ANSWER = "65556"

PART_TWO_DESCRIPTION = "correct bathroom code"
PART_TWO_ANSWER = "CB779"

# Assign space character to something 3 chars wide to make ascii keypads below easier to read
___ = " "


def _get_code(instructions, keypad, start_pos):
    """Navigates across a keypad using the provided instructions, starting at the specified
    starting position. Returns the code on the keypad the instructions yield."""

    code = ""
    x, y = start_pos

    for line in instructions:
        for step in line:
            # For each character in the instruction, move up, down, left, right accordingly, to
            # determine where your finger *might* end up
            if step == "U":
                next_coords = (x, y - 1)
            elif step == "D":
                next_coords = (x, y + 1)
            elif step == "R":
                next_coords = (x + 1, y)
            else:
                next_coords = (x - 1, y)

            # See what's in the next position you might move to
            next_y, next_x = next_coords
            next_char = keypad[next_y][next_x]

            # If there's a blank character, it's not a valid position (you're trying to move off
            # the edge of the keypad), so just stay where you are. If it's a valid character,
            # move to that position.
            if next_char != " ":
                x, y = next_coords

        # After each line of instructions, add the current character to the keypad code
        code += keypad[y][x]

    return code


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions):

    keypad = [
        [___, ___, ___, ___, ___],
        [___, "1", "2", "3", ___],
        [___, "4", "5", "6", ___],
        [___, "7", "8", "9", ___],
        [___, ___, ___, ___, ___],
    ]
    return _get_code(instructions, keypad, (2, 2))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(instructions):

    keypad = [
        [___, ___, ___, ___, ___, ___, ___],
        [___, ___, ___, "1", ___, ___, ___],
        [___, ___, "2", "3", "4", ___, ___],
        [___, "5", "6", "7", "8", "9", ___],
        [___, ___, "A", "B", "C", ___, ___],
        [___, ___, ___, "D", ___, ___, ___],
        [___, ___, ___, ___, ___, ___, ___],
    ]
    return _get_code(instructions, keypad, (1, 2))


# ----------------------------------------------------------------------------------------------


def run(input_file):

    instructions = get_input(input_file)

    part_one(instructions)
    part_two(instructions)

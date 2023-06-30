from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

DAY = 8
YEAR = 2016

PART_ONE_DESCRIPTION = "number of pixels that are on"
PART_ONE_ANSWER = 106

PART_TWO_DESCRIPTION = None
PART_TWO_ANSWER = None

PIXEL_ON = "#"
PIXEL_OFF = " "

_build_screen = lambda x, y: [list(PIXEL_OFF * x) for _ in range(y)]


def _simulate_screen(screen, instructions):
    """Simulate the screen by turning on and rotating pixels, using the provided instructions."""

    def _rect(x_size, y_size):
        """Creates a rectangle of ON pixels of size x*y in the top-left corner of the screen."""
        for y, x in nested_iterable(range(y_size), range(x_size)):
            screen[y][x] = PIXEL_ON

    def _rotate(sequence, steps):
        """Rotates a sequence by N steps, wrapping elements back to the beginning."""
        steps = steps % len(sequence)
        return sequence[-steps:] + sequence[:-steps]

    def _rot_row(row, steps):
        """Rotates a row on the screen by the specifies number of steps."""
        rotated = _rotate(screen[row], steps)
        screen[row] = rotated

    def _rot_col(col, steps):
        """Rotates a column on the screen by the specified number of steps."""
        col_to_rot = [screen[i][col] for i in range(len(screen))]
        rotated = _rotate(col_to_rot, steps)
        for i in range(len(screen)):
            screen[i][col] = rotated[i]

    for step in instructions:

        # Parse a rect command by extracting the x, y values
        if step.startswith("rect "):
            step = step.replace("rect ", "")
            x, y = [int(val) for val in step.split("x")]

            _rect(x, y)

        # Parse a rotate row command by extracting the row # and the steps
        if step.startswith("rotate row "):
            step = step.replace("rotate row ", "")
            y_part, steps = step.split(" by ")
            y = int(y_part.replace("y=", ""))
            steps = int(steps)

            _rot_row(y, steps)

        # Parse a rotate column command by extracting the column # and the steps
        if step.startswith("rotate column "):
            step = step.replace("rotate column ", "")
            x_part, steps = step.split(" by ")
            x = int(x_part.replace("x=", ""))
            steps = int(steps)

            _rot_col(x, steps)


def _render_screen(screen):
    for row in screen:
        print("".join(row))


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions, x, y):
    screen = _build_screen(x, y)
    _simulate_screen(screen, instructions)
    return sum(sum(1 for p in row if p == PIXEL_ON) for row in screen)


@aoc_output_formatter(YEAR, DAY, 2, ignore_return_val=True)
def part_two(instructions, x, y):
    screen = _build_screen(x, y)
    _simulate_screen(screen, instructions)
    _render_screen(screen)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    instructions = get_input(input_file)

    part_one(instructions, 50, 6)
    part_two(instructions, 50, 6)

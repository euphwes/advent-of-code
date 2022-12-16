from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

DAY = 2
YEAR = 2015

PART_ONE_DESCRIPTION = "square feet of wrapping paper"
PART_ONE_ANSWER = 1588178

PART_TWO_DESCRIPTION = "feet of ribbon"
PART_TWO_ANSWER = 3783758


def wrapping_paper_area(length, width, height):
    """Returns the wrapping paper area required to wrap a box with dimensions `length`, `width`,
    and `height`, with a little extra (the area of the smallest face)."""

    faces = [length * width, length * height, width * height]
    return 2 * sum(faces) + min(faces)


def ribbon_footage(length, width, height):
    """Returns the length of ribbon required to wrap the shortest perimeter of a box with
    dimensions `length`, `width`, and `height`, with a little extra for a box (the volume of the
    box, as length)."""

    perimeters = [2 * (length + width), 2 * (length + height), 2 * (width + height)]
    return min(perimeters) + (length * width * height)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(boxes):
    return sum(wrapping_paper_area(l, w, h) for l, w, h in boxes)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(boxes):
    return sum(ribbon_footage(l, w, h) for l, w, h in boxes)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    boxes = get_tokenized_input(input_file, "x", int)

    part_one(boxes)
    part_two(boxes)

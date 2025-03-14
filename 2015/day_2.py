from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 2
YEAR = 2015

PART_ONE_DESCRIPTION = "square feet of wrapping paper"
PART_ONE_ANSWER = 1588178

PART_TWO_DESCRIPTION = "feet of ribbon"
PART_TWO_ANSWER = 3783758


def wrapping_paper_area(length: int, width: int, height: int) -> int:
    """Return the area of wrapping required to wrap a box.

    The box has with dimensions `length`, `width`, and `height`, with a little extra
    (the area of the smallest face).
    """
    faces = [length * width, length * height, width * height]
    return 2 * sum(faces) + min(faces)


def ribbon_footage(length: int, width: int, height: int) -> int:
    """Return the length of ribbon required to wrap the shortest perimeter of a box.

    The box has dimensions `length`, `width`, and `height`, with a little extra for a box
    (the volume of the box, as length).
    """
    perimeters = [2 * (length + width), 2 * (length + height), 2 * (width + height)]
    return min(perimeters) + (length * width * height)


def _parse_boxes(raw_input: list[str]) -> list[tuple[int, ...]]:
    """Parse the input for a list of box definitions.

    Each line in the input is a box in the form "LxWxH", return a list of tuples
    of (L, W, H) for each box.
    """
    return [tuple([int(n) for n in line.split("x")]) for line in raw_input]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    boxes = _parse_boxes(raw_input)
    return sum(wrapping_paper_area(length, width, height) for length, width, height in boxes)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    boxes = _parse_boxes(raw_input)
    return sum(ribbon_footage(length, width, height) for length, width, height in boxes)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

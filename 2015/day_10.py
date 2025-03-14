from util.decorators import aoc_output_formatter

DAY = 10
YEAR = 2015

PART_ONE_DESCRIPTION = "length after 40 RLEs"
PART_ONE_ANSWER = 492982

PART_TWO_DESCRIPTION = "length after 50 RLEs"
PART_TWO_ANSWER = 6989950


def _run_length_encode(s: str) -> str:
    """Run-length encodes the provided string, and returns the result.

    Ex: 1102 -> 211012 (two 1, one 0, one two)
    """

    buffer = []

    count = 0
    current_char = None

    for char in s:
        if char == current_char:
            count += 1
        else:
            if current_char is not None:
                buffer.append(str(count))
                buffer.append(current_char)
            count = 1
            current_char = char

    buffer.append(str(count))
    buffer.append(current_char)

    return "".join(buffer)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: str) -> int | str | None:
    s = raw_input
    for _ in range(40):
        s = _run_length_encode(s)

    return len(s)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: str) -> int | str | None:
    s = raw_input
    for _ in range(50):
        s = _run_length_encode(s)

    return len(s)


def run(_: str) -> None:
    part_one("1321131112")
    part_two("1321131112")

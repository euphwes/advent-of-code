from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 8
YEAR = 2015

PART_ONE_DESCRIPTION = "answer"
PART_ONE_ANSWER = 1333

PART_TWO_DESCRIPTION = "answer"
PART_TWO_ANSWER = 2046


def _count_decoded(s: str) -> int:
    """Count the number of decoded characters in an encoded string."""

    count = 0

    # Strip the framing quotes, form an iterable over the stuff inside. Capture the iterable in
    # a named variable so we can `next(...)` it later to skip characters
    s = s[1:-1]
    s_iterable = enumerate(s)

    for i, char in s_iterable:
        count += 1

        # If this character is not a backslash, it's just the literal character.
        if char != "\\":
            continue

        # If it's \xAB, we need to skip over the next three escape sequence characters.
        if s[i + 1] == "x":
            for _ in range(3):
                next(s_iterable)

        # Otherwise it must be either \\ or \", the only other two escape sequences, so we can
        # just skip the next character.
        else:
            next(s_iterable)

    return count


def _count_encoded(s: str) -> int:
    """Count the number of characters in the encodes representation of the supplied string."""

    # Start with 2 for the framing quotes, then add 2 for literal " or \, and 1 for the rest
    return 2 + sum(2 if c in ("\\", '"') else 1 for c in s)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return sum(len(s) for s in raw_input) - sum(_count_decoded(s) for s in raw_input)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    return sum(_count_encoded(s) for s in raw_input) - sum(len(s) for s in raw_input)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

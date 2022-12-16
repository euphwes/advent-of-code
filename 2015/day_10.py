from util.decorators import aoc_output_formatter

DAY = 10
YEAR = 2015

PART_ONE_DESCRIPTION = "length after 40 RLEs"
PART_ONE_ANSWER = 492982

PART_TWO_DESCRIPTION = "length after 50 RLEs"
PART_TWO_ANSWER = 6989950


def _run_length_encode(s):
    """Run-length encodes the provided string, and returns the result."""

    buffer = list()

    count = 0
    current_char = None

    for i, char in enumerate(s):
        if char == current_char:
            count += 1
        else:
            if i > 0:
                buffer.append(str(count))
                buffer.append(current_char)
            count = 1
            current_char = char

    buffer.append(str(count))
    buffer.append(current_char)

    return "".join(buffer)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(s, n):
    for _ in range(n):
        s = _run_length_encode(s)
    return len(s)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(s, n):
    for _ in range(n):
        s = _run_length_encode(s)
    return len(s)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    input = "1321131112"

    part_one(input, 40)
    part_two(input, 50)

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 2
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def pairwise(myiter):
    for x in range(len(myiter) - 1):
        yield myiter[x], myiter[x + 1]


def is_safe(line):
    diffs = []
    for n1, n2 in pairwise(line):
        diffs.append(n1 - n2)
        diff = abs(n1 - n2)
        if not (diff >= 1 and diff <= 3):
            return False
    if all(x > 0 for x in diffs):
        return True
    elif all(x < 0 for x in diffs):
        return True
    return False


def truly_safe(line):
    if is_safe(line):
        return True

    for i in range(len(line)):
        test = line[:i] + line[i + 1 :]
        if is_safe(test):
            return True

    return False


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    return sum(1 for line in stuff if is_safe(line))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    return sum(1 for line in stuff if truly_safe(line))


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    stuffs = []
    for line in stuff:
        nline = []
        for n in line.split():
            nline.append(int(n))
        stuffs.append(nline)
    part_one(stuffs)

    stuff = get_input(input_file)
    stuffs = []
    for line in stuff:
        nline = []
        for n in line.split():
            nline.append(int(n))
        stuffs.append(nline)
    part_two(stuffs)

from util.decorators import aoc_output_formatter
from util.input import get_input

import re

DAY = 3
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    pattern = r"mul\(\d{1,3}\,\d{1,3}\)"

    n = 0

    for line in stuff:
        matches = re.findall(pattern, line)
        for match in matches:
            # print()
            # print(match)
            a, b = (int(n) for n in match[4:-1].split(","))
            n += a * b
            # print(f"adding {a*b}, sum now {n}")

    return n


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    pattern = r"mul\(\d{1,3}\,\d{1,3}\)|do\(\)|don't\(\)"

    n = 0

    enabled = True

    for line in stuff:
        matches = re.findall(pattern, line)
        for match in matches:
            print(match)
            if match == "do()":
                enabled = True
                continue
            if match == "don't()":
                enabled = False
                continue

            if not enabled:
                continue

            # print()
            # print(match)
            a, b = (int(n) for n in match[4:-1].split(","))
            n += a * b
            # print(f"adding {a*b}, sum now {n}")

    return n


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    # not 32081624
    # 32081624
    # 191183308
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

from itertools import combinations_with_replacement, product
from re import L
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 7
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _does_solve(answer, params, operators):
    running = params[0]

    for op, param in zip(operators, params[1:]):
        if running > answer:
            return False

        if op == "+":
            running += param
        elif op == "*":
            running *= param
        elif op == "|":
            running = int(str(running) + str(param))
        else:
            raise ValueError(f"unknown operator '{op}'")

    return running == answer


def _can_be_solved(line, operators):
    answer, raw_params = line.split(": ")
    answer = int(answer)
    params = [int(n) for n in raw_params.split()]

    num_operators = len(params) - 1

    for operators in product(operators, repeat=num_operators):
        if _does_solve(answer, params, operators):
            return True

    return False


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    foo = 0
    for line in stuff:
        if _can_be_solved(line, "+*"):
            answer, raw_params = line.split(": ")
            foo += int(answer)
    return foo


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    foo = 0
    for line in stuff:
        if _can_be_solved(line, "+*|"):
            answer, raw_params = line.split(": ")
            foo += int(answer)
    return foo


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

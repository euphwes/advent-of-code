from util.decorators import aoc_output_formatter
from util.input import get_input
from dataclasses import dataclass
from typing import Tuple
from math import floor
from util.algs import manhattan_distance
from z3 import And, Int, Ints, Or, Real, Reals, Solver, solve, unsat

DAY = 13
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

BUTTON_COST = {
    "A": 3,
    "B": 1,
}


@dataclass
class Machine:
    a_delta: Tuple[int, int]
    b_delta: Tuple[int, int]
    prize: Tuple[int, int]


def _parse_machines(stuff, with_correction=False):
    machines = []
    while stuff:
        raw_a = stuff.pop(0).replace("Button A: ", "").split(", ")
        raw_b = stuff.pop(0).replace("Button B: ", "").split(", ")
        raw_p = stuff.pop(0).replace("Prize: ", "").split(", ")

        ax = int(raw_a[0].replace("X+", ""))
        ay = int(raw_a[1].replace("Y+", ""))

        bx = int(raw_b[0].replace("X+", ""))
        by = int(raw_b[1].replace("Y+", ""))

        px = int(raw_p[0].replace("X=", ""))
        py = int(raw_p[1].replace("Y=", ""))

        extra = 10000000000000 if with_correction else 0

        machines.append(
            Machine(
                a_delta=(ax, ay),
                b_delta=(bx, by),
                prize=(px + extra, py + extra),
            )
        )

    return machines


def _min_cost(machine):
    options = []
    for a_presses in range(101):
        for b_presses in range(101):
            ax = a_presses * machine.a_delta[0]
            ay = a_presses * machine.a_delta[1]
            bx = b_presses * machine.b_delta[0]
            by = b_presses * machine.b_delta[1]

            if (ax + bx, ay + by) == machine.prize:
                options.append(a_presses * 3 + b_presses)
    return min(options) if options else 0


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    machines = _parse_machines(stuff)
    return sum(_min_cost(machine) for machine in machines)


def _solve_early_target(fmachine, early_target_loc):

    target = (early_target_loc, early_target_loc)

    machine = Machine(a_delta=fmachine.a_delta, b_delta=fmachine.b_delta, prize=target)

    # holds (a_presses, b_presses, dist to target, x, y of final position)
    options = []

    for a_presses in range(500):
        for b_presses in range(500):
            ax = a_presses * machine.a_delta[0]
            ay = a_presses * machine.a_delta[1]
            bx = b_presses * machine.b_delta[0]
            by = b_presses * machine.b_delta[1]

            cx = ax + bx
            cy = ay + by

            if cx > early_target_loc:
                continue
            if cy > early_target_loc:
                continue

            options.append(
                (a_presses, b_presses, manhattan_distance(target, (cx, cy)), cx, cy)
            )

    return min(options, key=lambda t: t[2])


def _min_cost_v2(machine, i):
    s = Solver()
    a_presses, b_presses = Ints("a_presses b_presses")

    """
    Button A: X+28, Y+94
    Button B: X+79, Y+69
    Prize: X=7377, Y=13189
    """

    s.add(
        a_presses * machine.a_delta[0] + b_presses * machine.b_delta[0]
        == machine.prize[0],
        a_presses * machine.a_delta[1] + b_presses * machine.b_delta[1]
        == machine.prize[1],
    )
    if s.check() == unsat:
        return 0

    r = s.model()
    return 3 * r[a_presses].as_long() + r[b_presses].as_long()


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    machines = _parse_machines(stuff, with_correction=True)
    return sum(_min_cost_v2(machine, i) for i, machine in enumerate(machines))


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    stuff = [line for line in stuff if line]
    part_one(stuff)

    stuff = get_input(input_file)
    stuff = [line for line in stuff if line]
    part_two(stuff)

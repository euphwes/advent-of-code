from itertools import combinations

from z3 import And, Int, Ints, Or, Real, Reals, Solver, solve

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def line(p1, p2):
    A = p1[1] - p2[1]
    B = p2[0] - p1[0]
    C = p1[0] * p2[1] - p2[0] * p1[1]
    return A, B, -C, p1, p2


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


def _parse_line(input_line):
    h1, h2 = input_line.split(" @ ")
    x1, y1, z1 = [int(x) for x in h1.split(", ")]
    dx, dy, dz = [int(x) for x in h2.split(", ")]
    x2 = x1 + dx
    y2 = y1 + dy
    z2 = z1 + dz
    return line((x1, y1), (x2, y2))


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    c = 0
    lines = [_parse_line(line) for line in stuff]
    for l1, l2 in combinations(lines, 2):
        inter = intersection(l1, l2)
        # if (
        #     inter
        #     and inter[0] >= 7
        #     and inter[0] <= 17
        #     and inter[1] >= 7
        #     and inter[1] <= 17
        # ):
        if (
            inter
            and inter[0] >= 200000000000000
            and inter[0] <= 400000000000000
            and inter[1] >= 200000000000000
            and inter[1] <= 400000000000000
        ):
            # only if intersection happens forward in time
            l1p1 = l1[3]
            l1p2 = l1[4]
            l2p1 = l2[3]
            l2p2 = l2[4]

            if l1p1[0] < l1p2[0]:
                if l1p1[0] > inter[0]:
                    continue
            else:
                if l1p1[0] < inter[0]:
                    continue

            if l2p1[0] < l2p2[0]:
                if l2p1[0] > inter[0]:
                    continue
            else:
                if l2p1[0] < inter[0]:
                    continue

            c += 1
            # print(intersection(l1, l2))
    return c


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    s = Solver()

    t1 = Int("t1")
    t2 = Int("t2")
    t3 = Int("t3")

    tx = Int("tx")
    ty = Int("ty")
    tz = Int("tz")
    tdx = Int("tdx")
    tdy = Int("tdy")
    tdz = Int("tdz")

    # s.add(
    #     tx + tdx * t1 == 19 - 2 * t1,
    #     ty + tdy * t1 == 13 + t1,
    #     tz + tdz * t1 == 30 - 2 * t1,
    #     tx + tdx * t2 == 18 - t2,
    #     ty + tdy * t2 == 19 - t2,
    #     tz + tdz * t2 == 22 - 2 * t2,
    #     tx + tdx * t3 == 20 - 2 * t3,
    #     ty + tdy * t3 == 25 - 2 * t3,
    #     tz + tdz * t3 == 34 - 4 * t3,
    # )
    s.add(
        tx + tdx * t1 == 385803404726014 - 192 * t1,
        ty + tdy * t1 == 386664184220541 - 149 * t1,
        tz + tdz * t1 == 365612177547870 - 36 * t1,
        tx + tdx * t2 == 67771006464582 + 280 * t2,
        ty + tdy * t2 == 193910554798739 + 136 * t2,
        tz + tdz * t2 == 21517103663672 + 426 * t2,
        tx + tdx * t3 == 334054450538558 + 84 * t3,
        ty + tdy * t3 == 356919582763697 - 25 * t3,
        tz + tdz * t3 == 188448277532212 - 48 * t3,
    )

    print(s.check())
    r = s.model()
    pos = [r[x].as_long() for x in [tx, ty, tz]]
    print(pos)
    return sum(pos)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    # part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

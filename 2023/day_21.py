from typing import List, Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 21
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _get_start(stuff):
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            if char == "S":
                return x, y
    raise ValueError()


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    start_x, start_y = _get_start(stuff)

    def _neighs(tcoord):
        tx, ty = tcoord
        for nx, ny in [
            (tx - 1, ty),
            (tx + 1, ty),
            (tx, ty - 1),
            (tx, ty + 1),
        ]:
            try:
                if stuff[ny][nx] in ".S":
                    yield nx, ny
            except IndexError:
                pass

    q: List[Tuple[Tuple[int, int], int]] = [((start_x, start_y), 0)]
    visited = set()

    reachable_in_64 = set()

    while q:
        coord, steps = q.pop(0)
        visited.add((coord, steps))

        if steps == 6:
            reachable_in_64.add(coord)
            continue

        for neigh in _neighs(coord):
            if (neigh, steps + 1) in visited:
                continue
            visited.add((neigh, steps + 1))
            q.append((neigh, steps + 1))

    return len(reachable_in_64)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    start_x, start_y = _get_start(stuff)
    start_x += 1
    # start_x, start_y = 65 + 66, 65 + 65

    size_y = len(stuff)
    size_x = len(stuff[0])
    print(f"{size_x=}, {size_y=}")

    def _neighs(tcoord):
        tx, ty = tcoord
        for nx, ny in [
            (tx - 1, ty),
            (tx + 1, ty),
            (tx, ty - 1),
            (tx, ty + 1),
        ]:
            try:
                if stuff[ny % size_y][nx % size_x] in ".S":
                    yield nx, ny
            except IndexError:
                pass

    # # for size in [6, 10, 50, 100, 500]:
    # # for size in [67]:  # right up against the edge
    for size in [65]:
        # for size in [197]:
        q: List[Tuple[Tuple[int, int], int]] = [((start_x, start_y), 0)]
        visited = set()

        reachable_in_64 = set()

        while q:
            coord, steps = q.pop(0)
            visited.add((coord, steps))

            if steps == size:
                reachable_in_64.add(coord)
                continue

            for neigh in _neighs(coord):
                if (neigh, steps + 1) in visited:
                    continue
                visited.add((neigh, steps + 1))
                q.append((neigh, steps + 1))

        print("\n---------\n\n")
        print(len(reachable_in_64))
        for y in range(start_y - 65, start_y + 65 + 1):
            for x in range(start_x - 65, start_x + 65 + 1):
                if (x, y) == (start_x, start_y):
                    print("S", end="")
                elif (x, y) in reachable_in_64:
                    print("O", end="")
                else:
                    char = stuff[y % size_y][x % size_x]
                    if char == "#":
                        char = "█"
                    if char in "S.":
                        char = " "
                    print(char, end="")
            print()

    # # size = 26501365
    # size = 130
    size = 65

    # # for size 65, correct answer 3874

    upper_bound = (2 * ((size // 2) + 1)) ** 2
    print(f"{upper_bound=}")

    # # There's 11 spaces in the interior which would be reachable in an odd number
    # # of steps, except that it's surrounded by walls. So we count that even though
    # # it won't have a rock on it itself.
    subtrs = 1

    for x in range(start_x - size, start_x + size + 1, 2):
        if stuff[start_y % size_y][x % size_x] == "#":
            subtrs += 1

    print(f"{len(reachable_in_64)=}")
    # print(f"start is at {start_x}, {start_y}")

    # going down
    for y in range(1, size + 1):
        # print(f"x range is {start_x - size + y} to {start_x + size + 1 - y}")
        for x in range(start_x - size + y, start_x + size + 1 - y, 2):
            # if num_rows_shown <= 30:
            # print(f"checking {x}, {(start_y + y)}")
            # num_rows_shown += 1
            if stuff[(start_y + y) % size_y][x % size_x] == "#":
                subtrs += 1

    # going up
    for y in range(1, size + 1):
        for x in range(start_x - size + y, start_x + size + 1 - y, 2):
            if stuff[(start_y - y) % size_y][x % size_x] == "#":
                subtrs += 1

    print(f"{subtrs=}")
    return upper_bound - subtrs

    # -------------------------------------
    # diamond big repeating diamond
    # substrs_overall = 4170
    # 5 of diamond A, 4 of diamond B
    #
    # # diamond A on odd rows
    substrs_a_center = 482
    substrs_a_off = 452
    #
    # which means there are 1760 substrs in the 4 diamond Bs
    # so 440 in each of diamond B
    #
    # diamond B on even rows
    substrs_b_a = 464
    substrs_b_off = 476  # ?
    # -------------------------------------

    f = """
                aa
              ba  bb
            aa  ab  aa
          ba  bb  ba  bb
        aa  ab  aa  ab  aa
      ba  bb  ba  bb  ba  bb
    aa  ab  aa  ab  aa  ab  aa
      bb  ba  bb  ba  bb  ba
        aa  ab  aa  ab  aa
          bb  ba  bb  ba
            aa  ab  aa
              bb  ba
                aa
    """
    assert f

    # each diamond is 131 wide

    # return (((26501365 - 65) // 131) * 2) + 1
    # 404601 diamonds across the center row

    size = 26501365
    upper_bound = (2 * ((size // 2) + 1)) ** 2

    # center row
    dia_count = 404601
    upper_bound -= substrs_a_center
    upper_bound -= ((dia_count - 1) // 2) * substrs_a_off
    upper_bound -= ((dia_count - 1) // 2) * substrs_a_center

    while dia_count > 1:
        dia_count -= 1
        # if dia_count % 1000 == 0:
        #     print(f"{dia_count=}")

        if dia_count % 2 == 1:
            for _ in range(2):
                upper_bound -= substrs_a_center
                upper_bound -= ((dia_count - 1) // 2) * substrs_a_off
                upper_bound -= ((dia_count - 1) // 2) * substrs_a_center
            continue

        else:
            for _ in range(2):
                upper_bound -= ((dia_count) // 2) * substrs_b_a
                upper_bound -= ((dia_count) // 2) * substrs_b_off

    return upper_bound
    # # -------------------------------------
    # #
    # size = 26501365
    # subtrs = 4170
    # upper_bound = (2 * ((size // 2) + 1)) ** 2
    # return upper_bound - ((134867**2) * subtrs)
    # #
    # # -------------------------------------

    # this is all bad, ignore me below

    # # -------------------------------------
    # #
    # size = 26501365
    # subtrs = 4170
    # upper_bound = (2 * ((size // 2) + 1)) ** 2
    # return upper_bound - ((202300**2) * subtrs)
    # #
    # # -------------------------------------

    # subtrs is 4170 for the large repeating diamond
    # return upper_bound - subtrs
    # return 26501365 % size_x ---> 65
    # return 26501365 // 65 ----> 407713

    # return 26501365 // 195


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)

    # not 531663940565956, too low
    # not 625302928475236, too low
    # not 683350879212724, too high
    # not 626437442587448
    # not 626473820802826

    # maybe 683351441877848

    # maybe 683360536296826 ** prefer this one with 4170 subtrs,
    # still not sure if (26501365) // 393 == 67433 is the right count for num large diamonds across

    # 626855792064274, not right
    # 624809517449274, not right
    # 624891368433874, not right, what the hell
    # 625628021226274 *****

    part_two(stuff)

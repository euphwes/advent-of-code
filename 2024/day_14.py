from dataclasses import dataclass

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 14
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int


def _parse_robots(raw_input: list[str]) -> list[Robot]:
    robots = []
    for line in raw_input:
        raw_loc, raw_delta = line.split()
        x, y = (int(n) for n in raw_loc.replace("p=", "").split(","))
        dx, dy = (int(n) for n in raw_delta.replace("v=", "").split(","))
        robots.append(Robot(x, y, dx, dy))

    return robots


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    # x_size = 11
    # y_size = 7
    x_size = 101
    y_size = 103
    max_x = x_size - 1
    max_y = y_size - 1
    robots = _parse_robots(raw_input)

    for _ in range(100):
        for r in robots:
            r.x = (r.x + r.dx) % x_size
            r.y = (r.y + r.dy) % y_size

    # count number of robots in each quadrant
    quadrants = [0, 0, 0, 0]
    for r in robots:
        if r.x == max_x // 2 or r.y == max_y // 2:
            continue

        if r.x < max_x // 2 and r.y < max_y // 2:
            quadrants[0] += 1
        elif r.x < max_x // 2 and r.y > max_y // 2:
            quadrants[1] += 1
        elif r.x >= max_x // 2 and r.y < max_y // 2:
            quadrants[2] += 1
        else:
            quadrants[3] += 1

    the_product = 1
    for q in quadrants:
        the_product *= q
    return the_product


def _print_robots(robots: list[Robot], ixx: int, x_size: int, y_size: int) -> None:
    grid = [["." for _ in range(x_size)] for _ in range(y_size)]
    for r in robots:
        grid[r.y][r.x] = "#"

    # append a newline to the file,
    # then write the grid line by line,
    # then write ixx
    with open("tree_maybe.txt", "a") as f:
        f.write("\n")
        for row in grid:
            f.write("".join(row) + "\n")
        f.write(f"{ixx}\n")


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    x_size = 101
    y_size = 103
    robots = _parse_robots(raw_input)

    hit_count = 0
    max_hits = 100

    def _check(bots):
        # populate a set with the locations of all the robots
        locations = set()
        for r in robots:
            locations.add((r.x, r.y))

        any_found = False
        for r in bots:
            disproved_diagonal = False
            x = r.x
            y = r.y
            for _ in range(4):
                x += 1
                y -= 1
                if (x, y) in locations:
                    continue
                disproved_diagonal = True
                break
            if not disproved_diagonal:
                any_found = True
                break
        return any_found

    for ixx in int_stream(1):
        for r in robots:
            r.x = (r.x + r.dx) % x_size
            r.y = (r.y + r.dy) % y_size

        # if quadrants[0] == quadrants[2] and quadrants[1] == quadrants[3]:
        # if ixx >= 350:
        # return ixx
        if _check(robots):
            _print_robots(robots, ixx, x_size, y_size)
            hit_count += 1
            if hit_count == max_hits:
                return None


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

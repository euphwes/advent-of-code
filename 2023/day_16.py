from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 16
YEAR = 2023

PART_ONE_DESCRIPTION = "total number of energized cells"
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

DP = dict()


def _move_light(light, contraption):
    global DP

    if light in DP:
        return DP[light]

    (x, y), direction = light

    if direction == "r":
        nx, ny = x + 1, y
    elif direction == "u":
        nx, ny = x, y - 1
    elif direction == "l":
        nx, ny = x - 1, y
    elif direction == "d":
        nx, ny = x, y + 1

    if (nx, ny) not in contraption:
        DP[light] = []
        return []

    next_directions = []

    cell = contraption[(nx, ny)]
    if cell == ".":
        # keep going the same way
        next_directions.append(direction)
    elif cell == "/":
        if direction == "r":
            next_directions.append("u")
        elif direction == "u":
            next_directions.append("r")
        elif direction == "l":
            next_directions.append("d")
        elif direction == "d":
            next_directions.append("l")
    elif cell == "\\":
        if direction == "r":
            next_directions.append("d")
        elif direction == "u":
            next_directions.append("l")
        elif direction == "l":
            next_directions.append("u")
        elif direction == "d":
            next_directions.append("r")
    elif cell == "|":
        if direction in ("r", "l"):
            next_directions.extend(("u", "d"))
        else:
            next_directions.append(direction)
    elif cell == "-":
        if direction in ("u", "d"):
            next_directions.extend(("l", "r"))
        else:
            next_directions.append(direction)

    DP[light] = [((nx, ny), d) for d in next_directions]
    return [((nx, ny), d) for d in next_directions]


def _print_energized(contraption, energized_cells):
    max_x = max(contraption.keys(), key=lambda x: x[0])[0]
    max_y = max(contraption.keys(), key=lambda x: x[1])[1]

    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in energized_cells:
                line += "#"
            else:
                line += "."
        print(line)


def _energize(contraption, starting_light):
    lights = [starting_light]
    energized_cells = set()

    from pprint import pprint

    while True:
        prev_cells = len(energized_cells)
        for _ in range(15):
            next_lights = []
            for light in lights:
                # print(light)
                new_lights = _move_light(light, contraption)
                next_lights.extend(new_lights)
                for new_light in new_lights:
                    energized_cells.add(new_light[0])
            lights = next_lights

        if prev_cells == len(energized_cells):
            break

    # _print_energized(contraption, energized_cells)
    return len(energized_cells)


def _parse_contraption(stuff):
    contraption = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            contraption[(x, y)] = char

    return contraption


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    contraption = _parse_contraption(stuff)
    return _energize(contraption, ((-1, 0), "r"))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    contraption = _parse_contraption(stuff)

    # get max y and  x around contraption
    # walk around the outside, with a direction pointing inside

    max_x = max(contraption.keys(), key=lambda x: x[0])[0]
    max_y = max(contraption.keys(), key=lambda x: x[1])[1]

    scores = []

    # along the top
    for x in range(max_x + 1):
        scores.append(_energize(contraption, ((x, -1), "d")))
    # along the bottom
    for x in range(max_x + 1):
        scores.append(_energize(contraption, ((x, max_y + 1), "u")))
    # along the left
    for y in range(max_y + 1):
        scores.append(_energize(contraption, ((-1, y), "r")))
    # along the right
    for y in range(max_y + 1):
        scores.append(_energize(contraption, ((max_x + 1, y), "l")))

    return max(scores)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

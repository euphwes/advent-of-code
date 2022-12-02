from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

# Dict to correlate a direction arrow to a change in (x, y) coordinates
__direction_mods = {
    '^': (0, -1),
    'v': (0, 1),
    '>': (1, 0),
    '<': (-1, 0),
}

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 3, 1, 'houses with presents', assert_answer=2592)
def part_one(directions):
    houses = set()
    houses.add((0, 0))

    x, y = 0, 0
    for direction in directions:
        dx, dy = __direction_mods[direction]
        x, y = x + dx, y + dy

        houses.add((x, y))

    return len(houses)


@aoc_output_formatter(2015, 3, 2, 'houses with presents', assert_answer=2360)
def part_two(directions):
    houses = set()
    houses.add((0, 0))

    x, y = 0, 0    # Santa's coordinates
    rx, ry = 0, 0  # Robo-Santa's coordinates
    for i, direction in enumerate(directions):
        dx, dy = __direction_mods[direction]

        # Santa and Robo-Santa take turns
        if (i % 2 == 0):
            x, y = x + dx, y + dy
            houses.add((x, y))
        else:
            rx, ry = rx + dx, ry + dy
            houses.add((rx, ry))

    return len(houses)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    directions = get_input(input_file)[0]

    part_one(directions)
    part_two(directions)

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import bidirectional_range, int_stream

from collections import defaultdict

DAY  = 14
YEAR = 2022

PART_ONE_DESCRIPTION = 'number of grains of sand before they enter the abyss'
PART_ONE_ANSWER = 692

PART_TWO_DESCRIPTION = 'number of grains of sand before source is blocked'
PART_TWO_ANSWER = 31706

#---------------------------------------------------------------------------------------------------

AIR  = '.'
ROCK = '#'
SAND = 'o'

SAND_SOURCE = (500, 0)


def _get_cave_map(cave_walls_info):
    """ Parses the input file and returns a dictionary of cave coordinates to
    what's there, starting with empty except where the input file specifies
    there is rock. """

    cave_map = defaultdict(lambda: '.')

    while cave_walls_info:
        wall_info = cave_walls_info.pop(0)
        coords = wall_info.split(' -> ')

        # On each line, iterate between each adjacent pair of coordinates and
        # fill those coordinates with rock.
        stop = coords.pop(0)
        while coords:
            start = stop
            stop = coords.pop(0)

            stop_x, stop_y = (int(n) for n in stop.split(','))
            start_x, start_y = (int(n) for n in start.split(','))

            for x in bidirectional_range(start_x, stop_x, inclusive=True):
                for y in bidirectional_range(start_y, stop_y, inclusive=True):
                    cave_map[(x, y)] = ROCK

    return cave_map


def _fill_with_sand(cave_map, end_sim_check_fn):
    """ Given a cave map, simulates a single particle of sand falling from the source until it comes
    to rest, or a condition is met to cause the simulation to end. """

    # Sand particles fall in from the source
    sand_x, sand_y = SAND_SOURCE

    # Keeping making the sand fall further down until it doesn't anymore.
    while True:
        did_fall = False

        # First check if the sand can fall straight down, and then down+left, and finally down+right
        for dx in (0, -1, 1):
            if cave_map[(sand_x+dx, sand_y+1)] == AIR:
                # The sand can fall this direction. Update current position and mark that it fell.
                sand_x += dx
                sand_y += 1
                did_fall = True

                # Don't check the other fall positions, the earliest that works takes precedence.
                break

        # Check if we've reached the condition that indicates we should stop simulating the sand.
        end_sim_check_fn(sand_x, sand_y)

        # If the sand didn't fall, break out and place the sand at its final position.
        if not did_fall:
            break

    cave_map[(sand_x, sand_y)] = SAND
    return cave_map


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(cave_walls_info):

    cave_map = _get_cave_map(cave_walls_info)
    lowest_wall = max(y for _, y in cave_map.keys())

    # Run the simulation until a sand particle falls below the lowest rock that we know about
    # in the cave.

    class SandFallsForever(Exception):
        pass

    def stop_if_falling_into_abyss(sand_x, sand_y):
        if sand_y > lowest_wall:
            raise SandFallsForever()

    try:
        for i in int_stream():
            cave_map = _fill_with_sand(cave_map, stop_if_falling_into_abyss)
    except SandFallsForever:
        # Sand is now falling into the abyss, return how many particles came to rest before that happened.
        return i


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(cave_walls_info):

    cave_map = _get_cave_map(cave_walls_info)

    # Oops, the cave actually has an infinite floor 2 units below the lowest rock that we knew
    # about from the input file.
    lowest_wall = max(y for _, y in cave_map.keys())
    floor = lowest_wall + 2

    # Sand can only fall as far left/right as it does straight down. Since the sand starts at
    # SAND_SOURCE (y = 0), and the floor is at `floor`, the sand can only fall at most `floor`
    # units left or right of the x coordinate of the source.
    #
    # Fill in the cave map with the true floor of the cave, a straight line at y = `floor`,
    # x between SAND_SOURCE's x coordinate +/- `floor`.
    source_x = SAND_SOURCE[0]
    for fx in bidirectional_range(source_x-floor, source_x+floor, inclusive=True):
        cave_map[(fx, floor)] = ROCK

    # The sand simulation runs until sand clogs the source by having a particle stop there.
    class SandClogsTheSource(Exception):
        pass

    def stop_if_clogging_source(sand_x, sand_y):
        if (sand_x, sand_y) == SAND_SOURCE:
            raise SandClogsTheSource()

    try:
        for i in int_stream():
            cave_map = _fill_with_sand(cave_map, stop_if_clogging_source)
    except SandClogsTheSource:
        # Sand is clogging the source, return how many particles of sand fell to make that happen.
        return i+1

#---------------------------------------------------------------------------------------------------

def run(input_file):

    cave_walls_info = get_input(input_file)
    part_one(cave_walls_info)

    cave_walls_info = get_input(input_file)
    part_two(cave_walls_info)
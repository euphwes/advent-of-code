from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable
from util.structures import get_neighbors_of

#---------------------------------------------------------------------------------------------------

LIGHT_ON = '#'
LIGHT_OFF = '.'


def __create_blank_light_grid(width, height):
    """ Creates a blank light grid with the provided width and height. """

    return [[None] * width for _ in range(height)]


def __count_nearby_on_lights(x, y, lights):
    """ Counts the number of lights neighboring the provided position which are on. """

    return sum(1 for light in get_neighbors_of(x, y, lights) if light == LIGHT_ON)


def __count_total_lights_on(lights):
    """ Returns a count of lights which are on in the light grid. """

    lights_on = 0
    for row in lights:
        for light in row:
            if light == LIGHT_ON:
                lights_on += 1

    return lights_on


def __animate_lights(lights, handle_stuck_lights = False):
    """ Evaluates the light grid and returns its state at the next step in time. """

    width = len(lights[0])
    height = len(lights)

    corner_lights = [
        (0, 0),
        (0, height-1),
        (width-1, 0),
        (width-1, height-1)
    ]

    # Create a new array which hold the state of the lights at the next step in time
    new_lights = __create_blank_light_grid(width, height)

    # Iterate over each light and evaluate it to determine what its next state will be
    for x, y in nested_iterable(range(width), range(height)):
        if handle_stuck_lights and (x, y) in corner_lights:
            new_lights[y][x] = LIGHT_ON
            continue

        # Count the number of nearby lights which are on.
        nearby_on_lights = __count_nearby_on_lights(x, y, lights)

        if lights[y][x] == LIGHT_OFF:
            new_lights[y][x] = LIGHT_ON if nearby_on_lights == 3 else LIGHT_OFF
            continue

        new_lights[y][x] = LIGHT_ON if nearby_on_lights in (2, 3) else LIGHT_OFF

    return new_lights

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 18, 1, "number of lights on", assert_answer=821)
def part_one(lights):

    for _ in range(100):
        lights = __animate_lights(lights, handle_stuck_lights = False)

    return __count_total_lights_on(lights)


@aoc_output_formatter(2015, 18, 2, 'number of lights on', assert_answer=886)
def part_two(lights):

    # Ensure the 4 corner lights start on
    max_x = len(lights[0]) - 1
    max_y = len(lights) - 1

    lights[0][0]         = LIGHT_ON
    lights[max_y][0]     = LIGHT_ON
    lights[0][max_x]     = LIGHT_ON
    lights[max_y][max_x] = LIGHT_ON

    for _ in range(100):
        lights = __animate_lights(lights, handle_stuck_lights = True)

    return __count_total_lights_on(lights)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one([list(line) for line in get_input(input_file)])
    part_two([list(line) for line in get_input(input_file)])

from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

#---------------------------------------------------------------------------------------------------

def _follow_path(instructions):
    """ Iterate over the instructions, yielding a coordinate pair for each city block visited. """
    # Directions: 0, 1, 2, 3 = N, E, S, W
    x, y = 0, 0
    direction = 0

    yield (x, y)

    for step in instructions:
        turn = step[0]
        direction = (direction + (1 if turn == 'R' else -1)) % 4

        distance = int(step[1:])
        for _ in range(distance):
            if direction == 0:
                y += 1
            elif direction == 1:
                x += 1
            elif direction == 2:
                y -= 1
            else:
                x -= 1

            yield (x, y)


def _manahattan_distance(coords):
    x, y = coords
    return abs(x) + abs(y)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2016, 1, 1, 'distance to Easter Bunny HQ')
def part_one(instructions):
    for coords in _follow_path(instructions):
        pass
    return _manahattan_distance(coords)


@aoc_output_formatter(2016, 1, 2, 'distance to Easter Bunny HQ real location')
def part_two(instructions):
    locations = set()
    for coords in _follow_path(instructions):
        if coords in locations:
            return _manahattan_distance(coords)
        locations.add(coords)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = get_tokenized_input(input_file, ', ')[0]

    part_one(instructions)
    part_two(instructions)

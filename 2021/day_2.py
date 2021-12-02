from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _parse_line(entry):
    direction, amount = entry.split(' ')
    amount = int(amount)
    return direction, amount


@aoc_output_formatter(2021, 2, 1, 'product of horizontal position and depth')
def part_one(entries):
    x, y = 0, 0
    for dir, amt in [_parse_line(line) for line in entries]:
        if dir == 'up':
            x -= amt
        elif dir == 'down':
            x += amt
        else:
            y += amt
    return x * y


@aoc_output_formatter(2021, 2, 2, 'product of correct horizontal position and depth')
def part_two(entries):
    x, y, aim = 0, 0, 0
    for dir, amt in [_parse_line(line) for line in entries]:
        if dir == 'up':
            aim -= amt
        elif dir == 'down':
            aim += amt
        else:
            x += amt
            y += (aim * amt)
    return x * y

#---------------------------------------------------------------------------------------------------

def run(input_file):

    entries = get_input(input_file)

    part_one(entries)
    part_two(entries)

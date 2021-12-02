from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2021, 1, 1, 'number of times a depth measurement increases')
def part_one(measurements):
    count = 0
    for i in range(1, len(measurements)):
        if measurements[i] > measurements[i-1]:
            count += 1
    return count


@aoc_output_formatter(2021, 1, 2, 'number of times a sliding window depth measurement increases')
def part_two(measurements):
    count = 0
    for i in range(2, len(measurements)):
        curr_window = sum(measurements[i-3:i])
        prev_window = sum(measurements[i-4:i-1])
        if curr_window > prev_window:
            count += 1
    return count

#---------------------------------------------------------------------------------------------------

def run(input_file):

    measurements = [int(line) for line in get_input(input_file)]

    part_one(measurements)
    part_two(measurements)

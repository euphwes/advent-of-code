from util.decorators import aoc_output_formatter
from util.iter import int_stream

#---------------------------------------------------------------------------------------------------

def _diagonal_coords_stream():
    for target_sum in int_stream(2):
        for y in int_stream(1, target_sum-1):
            yield (target_sum - y, y)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 25, 1, 'code at target coordinates')
def part_one(target_x, target_y):
    code = 20151125
    for x, y in _diagonal_coords_stream():
        if (x, y) == (target_x, target_y):
            return code
        code = (code * 252533) % 33554393

#---------------------------------------------------------------------------------------------------

def run(input_file):
    part_one(2978, 3083)

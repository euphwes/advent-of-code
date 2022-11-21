from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2017, 17, 1, 'value following 2017')
def part_one(step_size):
    buffer = [0]
    curr_index = 0
    for value in range(1, 2018):
        curr_index = (curr_index + step_size) % len(buffer)
        buffer = buffer[:curr_index+1] + [value] + buffer[curr_index+1:]
        curr_index = (curr_index + 1) % len(buffer)
    return buffer[curr_index + 1]


@aoc_output_formatter(2017, 17, 2, 'value following 0, after 50M insertions')
def part_two(step_size):

    # Because the solution is the value that follows 0, and 0 always stays in the first position,
    # we only need to keep track of the value after 0 at any given time.
    value_after_0 = 0

    # Track the length of the buffer as it grows, as well as where we are in the buffer, even though
    # we aren't actually tracking the buffer itself.
    buffer_len = 1
    curr_index = 0

    for value in range(1, 50_000_001):

        # Step `size_size` away, wrapping back to the front in a circular fashion
        curr_index = (curr_index + step_size) % buffer_len

        # If we end up at the 0th index, we'd be inserting right after it, which will be the latest
        # value that follows 0, so keep track of that.
        if curr_index == 0:
            value_after_0 = value

        # Regardless of where the index ended up, the buffer is now 1 larger. Increment the index
        # to point at the value we just inserted.
        buffer_len += 1
        curr_index = (curr_index + 1) % buffer_len

    return value_after_0


#---------------------------------------------------------------------------------------------------

def run(input_file):

    step_size = 344

    part_one(step_size)
    part_two(step_size)

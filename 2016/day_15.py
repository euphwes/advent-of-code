from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

#---------------------------------------------------------------------------------------------------

def _parse_input(lines):
    """ Parse the input file to figure out how many positions and the starting position for each
    disc. """

    # Key: disc number
    # Value: tuple of (start_position, num_positions)
    disc_info = dict()

    # Example line:
    # Disc #3 has 19 positions; at time=0, it is at position 2.
    for line in lines:
        raw_disc_num_pos, raw_start_pos = line.split('; at time=0, it is at position ')
        raw_disc, raw_pos = raw_disc_num_pos.split(' has ')
        disc_num = int(raw_disc.replace('Disc #', ''))
        num_positions = int(raw_pos.replace(' positions', ''))
        start_pos = int(raw_start_pos.replace('.', ''))
        disc_info[disc_num] = (start_pos, num_positions)

    return disc_info


def _will_capsule_pass_through_at_ix(disc_info, ix):
    """ Simulates the disc positions and determines if a capsule will pass through at a given
    time index. """

    # For each time delta between the provided time index and the distance of each disc...
    # (disc 1 is at ix + 1s, disc 5 is at ix + 5s, etc)
    for delta in range(1, max(disc_info.keys())+1):

        # Grab the disc info, and figure out its current position based on the starting position and
        # how much total time has elapsed.
        disc_start, disc_num_pos = disc_info[delta]
        disc_pos = (disc_start + ix + delta) % disc_num_pos

        # If the disc is not aligned with the falling capsule, the capsule will bounce and not
        # pass through.
        if disc_pos != 0:
            return False

    # The capsule aligned with all the discs and made it through.
    return True


@aoc_output_formatter(2016, 15, 1, 'first time index to get a capsule')
def part_one(disc_info):
    for n in int_stream(0):
        if _will_capsule_pass_through_at_ix(disc_info, n):
            return n


@aoc_output_formatter(2016, 15, 2, 'first time index to get a capsule with new disc')
def part_two(disc_info):
    for n in int_stream(0):
        if _will_capsule_pass_through_at_ix(disc_info, n):
            return n

#---------------------------------------------------------------------------------------------------

def run(input_file):

    lines = get_input(input_file)
    disc_info = _parse_input(lines)

    part_one(disc_info)

    disc_info[7] = (0, 11)
    part_two(disc_info)

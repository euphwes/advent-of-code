from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _count_characters_until_marker_found(message, unique_char_count):
    """ Returns the number of characters processed until the 'start of message' marker is found,
    which are `unique_char_count` consecutive different characters. """

    # We're peeking ahead `unique_char_count` so we can only check the message starting that many
    # characters before the end.
    max_ix_to_check = len(message)-unique_char_count

    for i in range(max_ix_to_check):
        # Starting at the current position, peek ahead to capture the correct number of characters
        next_n_chars = message[i:i+unique_char_count]

        # If the number of distinct characters is the number of required characters to form a
        # "start of message" marker, return the total number of characters found until we reach
        # that last character in the marker.
        if len(set(next_n_chars)) == unique_char_count:
            return i + unique_char_count


@aoc_output_formatter(2022, 6, 1, 'characters before 4-character marker is found', assert_answer=1155)
def part_one(stuff):
    return _count_characters_until_marker_found(stuff, 4)


@aoc_output_formatter(2022, 6, 2, 'characters before 14-character marker is found', assert_answer=2789)
def part_two(stuff):
    return _count_characters_until_marker_found(stuff, 14)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    message = get_input(input_file)[0]

    part_one(message)
    part_two(message)

from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 6
YEAR = 2016

PART_ONE_DESCRIPTION = "error-corrected message"
PART_ONE_ANSWER = "zcreqgiv"

PART_TWO_DESCRIPTION = "modified reptition error-corrected message"
PART_TWO_ANSWER = "pljvorrk"


def _get_error_corrected_message(messages, is_modified_repetition_code):
    """Returns the error corrected message based on the received messages and the frequencies of
    letters occuring in each position. If it's a modified repeition code, the correct letter is
    the least-frequent letter to occur in each position, otherwise it's the most frequent."""

    error_corrected_message = ""
    for i in range(len(messages[0])):

        # Accumulate letter frequencies for the letters in position i across all messages
        letter_frequency = defaultdict(int)
        for message in messages:
            letter_frequency[message[i]] += 1

        # Turn the letter frequencies into a list of tuples if the form (count, letter) and sort
        # by count, either in ascending or descending order of frequency depending on whether
        # this is a modified repetition code.
        letter_freq_pairs = [
            (count, letter) for letter, count in letter_frequency.items()
        ]

        is_reversed_sort = not is_modified_repetition_code
        letter_freq_pairs.sort(
            key=lambda count_letter: count_letter[0], reverse=is_reversed_sort
        )

        # Append the most frequent character for position i to the error_corrected_message
        error_corrected_message += letter_freq_pairs[0][1]

    return error_corrected_message


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(messages):
    return _get_error_corrected_message(messages, False)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(messages):
    return _get_error_corrected_message(messages, True)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    messages = get_input(input_file)

    part_one(messages)
    part_two(messages)

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of calibration values only considering digits"
PART_ONE_ANSWER = 54450

PART_TWO_DESCRIPTION = "sum of calibration values also considering number words"
PART_TWO_ANSWER = 54265


DIGITS = set("0123456789")


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(calibration_document):
    # Maintain a list of the calibration values for each line in the document
    calibration_values = list()

    # For each line in the document...
    for line in calibration_document:
        # Read through the line and keep only the digits characters in a list.
        # Example: 'foo1bar3hello9yes' --> ['1', '3', '9']
        digits = [x for x in line if x in DIGITS]

        # Get the first and last digits (they're still strings at this point).
        # When you use "negative indexing" like we're doing below for final_digit, it counts
        # backwards from the first element and wraps around to the final one. So indexing
        # digits[-1] counts backwards 1 from the first character, wrapping around, giving us
        # the last character.
        first_digit = digits[0]
        final_digit = digits[-1]

        # Combine the first and last digit to get a string version of the calibration number
        raw_calibration_num = first_digit + final_digit

        # Turn it into an actual integer with int(...)
        calibration_num = int(raw_calibration_num)

        # Add it to the list of calibration values
        calibration_values.append(calibration_num)

    # Now we're done reading through the document, we have a list of all the calibration values
    # for each line in the document, and we can just return its sum, which is the part 1 answer.
    return sum(calibration_values)


WORD_DIGITS_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def _get_first_num(line) -> str:
    """Returns the first number found in the line, whether it's an actual digit 1-9, or a word
    representing that digit.

    Ex: hello7there9 --> 7
    Ex: fooseventhere9 --> 7
    """

    # So we're going to inspect the line by considering ever-increasing "windows" at the start
    # of the line, until we find either a digit or a word representing a digit in there.
    #
    # Ex: given this line: xone2
    # First we'd look at "x" (no number in here)
    # Then "xo" (no number in here)
    # Then "xon" (no number in here)
    # Then "xone" (we found the word "one", which corresponds to 1)
    #
    # Another ex: given this line: ab123
    # First we'd look at "a" (no number in here)
    # Then "ab" (no number in here)
    # Then "ab1" (we found 1)

    # For every window-ending index, starting at the first character and going up to the full
    # size of the line...
    for window_end in range(1, len(line) + 1):
        # Get the substring of the line that starts at the beginning and ends with that index
        substring = line[:window_end]

        # If the last character of that substring is a digit, return that digit
        if substring[-1] in DIGITS:
            return substring[-1]

        # Otherwise if the substring ends with any of the words that correspond to digits,
        # return that digit.
        for number_word in WORD_DIGITS_MAP.keys():
            if substring.endswith(number_word):
                return WORD_DIGITS_MAP[number_word]

        # If we make it here, we haven't found a number yet, try a larger window.

    raise ValueError("Couldn't find a number in the line")


def _get_final_num(line):
    """Returns the final number found in the line, whether it's an actual digit 1-9, or a word
    representing that digit.

    Ex: hello7there9 --> 9
    Ex: foo7thereightx --> 8
    """

    # So we're going to inspect the line by considering ever-increasing "windows" at the end
    # of the line, until we find either a digit or a word representing a digit in there.
    #
    # Ex: given this line: yonex
    # First we'd look at "x" (no number in here)
    # Then "ex" (no number in here)
    # Then "nex" (no number in here)
    # Then "onex" (we found the word "one", which corresponds to 1)
    #
    # Another ex: given this line: 123ba
    # First we'd look at "a" (no number in here)
    # Then "ba" (no number in here)
    # Then "3ba" (we found 3)

    # For every window-starting index, starting at the last character and going up to the full
    # size of the line...
    for window_start in range(1, len(line) + 1):
        # Get the substring of the line that's the last N characters of that line
        substring = line[-window_start:]

        # If the first character of that substring is a digit, return that digit
        if substring[0] in DIGITS:
            return substring[0]

        # Otherwise if the substring starts with any of the words that correspond to digits,
        # return that digit.
        for number_word in WORD_DIGITS_MAP.keys():
            if substring.startswith(number_word):
                return WORD_DIGITS_MAP[number_word]

    raise ValueError("Couldn't find a number in the line")


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(calibration_document):
    # Maintain a list of the calibration values for each line in the document
    calibration_values = list()

    # For each line in the document...
    for line in calibration_document:
        # Get the first and last digits with the helper functions defined above.
        # These consider words like "one", "three", etc, as well as the digits themselves.
        first_digit = _get_first_num(line)
        final_digit = _get_final_num(line)

        # Combine the first and last digit to get a string version of the calibration number
        raw_calibration_num = first_digit + final_digit

        # Turn it into an actual integer with int(...)
        calibration_num = int(raw_calibration_num)

        # Add it to the list of calibration values
        calibration_values.append(calibration_num)

    # Now we're done reading through the document, we have a list of all the calibration values
    # for each line in the document, and we can just return its sum, which is the part 2 answer.
    return sum(calibration_values)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    calibration_document = get_input(input_file)

    part_one(calibration_document)
    part_two(calibration_document)

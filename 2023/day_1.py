from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of calibration values only considering digits"
PART_ONE_ANSWER = 54450

PART_TWO_DESCRIPTION = "sum of calibration values also considering number words"
PART_TWO_ANSWER = 54265


DIGITS = set("0123456789")
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

    for window_end in range(1, len(line) + 1):
        substring = line[:window_end]

        # If the last character of that substring is a digit, return that digit
        if substring[-1] in DIGITS:
            return substring[-1]

        # Otherwise if the substring ends with any of the words that correspond to digits,
        # return that digit.
        for number_word in WORD_DIGITS_MAP.keys():
            if substring.endswith(number_word):
                return WORD_DIGITS_MAP[number_word]

    raise ValueError("Couldn't find a number in the line")


def _get_final_num(line):
    """Returns the final number found in the line, whether it's an actual digit 1-9, or a word
    representing that digit.

    Ex: hello7there9 --> 9
    Ex: foo7thereightx --> 8
    """

    for window_start in range(1, len(line) + 1):
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


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(calibration_document):
    calibration_values = list()

    for line in calibration_document:
        digits = [x for x in line if x in DIGITS]
        calibration_values.append(int(digits[0] + digits[-1]))

    return sum(calibration_values)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(calibration_document):
    calibration_values = list()

    for line in calibration_document:
        first_digit = _get_first_num(line)
        final_digit = _get_final_num(line)
        calibration_values.append(int(first_digit + final_digit))

    return sum(calibration_values)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    calibration_document = get_input(input_file)

    part_one(calibration_document)
    part_two(calibration_document)

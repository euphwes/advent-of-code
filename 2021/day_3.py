from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _get_bit_counts_at_index(i, lines):
    """ Returns a tuple, the count of 0s and 1s at the provided index. """
    counts = defaultdict(int)
    for line in lines:
        counts[line[i]] += 1

    return counts['0'], counts['1']


@aoc_output_formatter(2021, 3, 1, 'submarine power consumption')
def part_one(diagnostic_report):
    gamma_rate = ''
    epsilon_rate = ''
    report_line_length = len(diagnostic_report[0])

    for i in range(report_line_length):
        # Count 0/1 rates for each index individually
        c0, c1 = _get_bit_counts_at_index(i, diagnostic_report)

        # gamma rate's i-th bit is the most common bit at that index
        # epsilon rate's i-th bit is the least common bit at that index
        if c1 > c0:
            gamma_rate += '1'
            epsilon_rate += '0'
        else:
            gamma_rate += '0'
            epsilon_rate += '1'

    return int(gamma_rate, 2) * int(epsilon_rate, 2)


@aoc_output_formatter(2021, 3, 2, 'submarine life support rating')
def part_two(diagnostic_report):
    report_line_length = len(diagnostic_report[0])

    # Copy the diagnostic_report since we're modifying it while determining O2 generator rating
    o2_report_copy = [l for l in diagnostic_report]

    o2_generator_rating = ''
    for i in range(report_line_length):
        # While building up the O2 generator rating, omit any lines from the report which do not
        # match what the rating is so far.
        o2_report_copy = [line for line in o2_report_copy if line.startswith(o2_generator_rating)]

        # If there's only one line left in the diagnostic report, that's the O2 generator rating
        if len(o2_report_copy) == 1:
            o2_generator_rating = o2_report_copy[0]
            break

        # Count 0/1 rates for each index individually
        # O2 generator rating's i-th bit is the most common bit at that index, with 1 as tie-breaker
        c0, c1 = _get_bit_counts_at_index(i, o2_report_copy)
        if c1 >= c0:
            o2_generator_rating += '1'
        else:
            o2_generator_rating += '0'

    # Copy the diagnostic_report since we're modifying it while determining CO2 scrubber rating
    co2_report_copy = [l for l in diagnostic_report]

    co2_scrubber_rating = ''
    for i in range(report_line_length):
        # While building up the CO2 scrubber rating, omit any lines from the report which do not
        # match what the rating is so far.
        co2_report_copy = [line for line in co2_report_copy if line.startswith(co2_scrubber_rating)]

        # If there's only one line left in the diagnostic report, that's the CO2 scrubber rating
        if len(co2_report_copy) == 1:
            co2_scrubber_rating = co2_report_copy[0]
            break

        # Count 0/1 rates for each index individually
        # CO2 scrubber rating's i-th bit is the least common bit at that index, with 0 as tie-breaker
        c0, c1 = _get_bit_counts_at_index(i, co2_report_copy)
        if c1 >= c0:
            co2_scrubber_rating += '0'
        else:
            co2_scrubber_rating += '1'

    return int(o2_generator_rating, 2) * int(co2_scrubber_rating, 2)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    diagnostic_report = [line for line in get_input(input_file) if line]

    part_one(diagnostic_report)
    part_two(diagnostic_report)

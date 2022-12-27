from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 25
YEAR = 2022

PART_ONE_DESCRIPTION = "SNAFU representation of sum of fuel requirements"
PART_ONE_ANSWER = "2==221=-002=0-02-000"


SNAFU_TO_DECIMAL_DIGITS = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

DECIMAL_TO_SNAFU_DIGITS = {v: k for k, v in SNAFU_TO_DECIMAL_DIGITS.items()}


def _to_snafu(decimal_number):
    """Convert a decimal number to its SNAFU representation."""

    # First convert the decimal number to a standard base-5 number (with digits 0-4).
    power_of_5_needed = 0
    while True:
        if 5**power_of_5_needed > decimal_number:
            power_of_5_needed -= 1
            break
        power_of_5_needed += 1

    standard_base_5_number = ""

    power = power_of_5_needed
    while power > 0:
        base_5_multiplyer = 5**power

        # Find the digit at the current power of 5 by taking the integer division of the decimal
        # number and this power of 5.
        digit = decimal_number // base_5_multiplyer
        standard_base_5_number += str(digit)

        # Get the remainder after the divison, which we pass to the next lower power of 5.
        decimal_number = decimal_number % base_5_multiplyer
        power -= 1

    standard_base_5_number += str(decimal_number)

    # For each digit in the standard base-5 representation, adjust it to become SNAFU.
    # For example, we can't have a digit higher than 2 in SNAFU, so anything higher we subtract
    # 5 from it (4 becomes -1 aka "-", or 3 becomes -2 aka "=") and to balance it, since we
    # subtracted the (decimal) value of 5 from this digit, we have to add "1" to the next larger
    # digit to add the equivalent decimal value of 5 back.
    snafu_power_order = list()

    do_carry = False
    for digit in reversed([int(digit) for digit in standard_base_5_number]):
        if do_carry:
            digit += 1

        if digit >= 3:
            digit -= 5
            do_carry = True
        else:
            do_carry = False

        snafu_power_order.append(DECIMAL_TO_SNAFU_DIGITS[digit])

    # The SNAFU number is in a reverse representation, lowest power of 5 to highest, so reverse
    # that back and then join it into a single string.
    return "".join(reversed(snafu_power_order))


def _to_decimal(snafu_number):
    """Convert a SNAFU number to its decimal equivalent."""

    # Convert to decimal by summing the increasing powers of 5 (as SNAFU is a base-5 system)
    decimal_sum = 0
    for i, digit in enumerate(reversed(snafu_number)):
        decimal_sum += (5**i) * SNAFU_TO_DECIMAL_DIGITS[digit]

    return decimal_sum


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(fuel_reqs):

    decimal_sum = sum(_to_decimal(fuel) for fuel in fuel_reqs)
    return _to_snafu(decimal_sum)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    fuel_reqs = get_input(input_file)
    part_one(fuel_reqs)

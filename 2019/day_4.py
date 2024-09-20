from util.input import get_input
from util.decorators import aoc_output_formatter


DAY = 4
YEAR = 2019

PART_ONE_DESCRIPTION = "number of valid passwords"
PART_ONE_ANSWER = 1246

PART_TWO_DESCRIPTION = "number of valid passwords"
PART_TWO_ANSWER = 814


# Specifies the password must have a run of the same consecutive digit, of exactly length 2
has_run_of_exactly_two = lambda digit_runs: 2 in digit_runs

# Specifies the password must have a run of the same consecutive digit, of at least length 2
has_run_of_at_least_two = lambda digit_runs: any(n >= 2 for n in digit_runs)


def _validate_password(password, digit_run_check):
    """Validates a password by ensuring that no two adjacent digits are descending from
    left to right, and also that the password contains a run of consecutive digits that
    meet the requirements specified by the provided `digit_run_check` predicate."""

    # Break the password into a list of individual digits
    password = [int(n) for n in str(password)]

    # For each distinct digit visited from left-to-right, record the length
    # of the run of that digit. Ex: 344555 --> [1, 2, 3] (1x 3, 2x 4, 3x 5)
    digit_runs = list()

    # Maintain the length of the current run, and what the previous visited digit was
    curr_run = 1
    prev_digit = None

    for i in range(len(password)):
        curr_digit = password[i]

        # If this digit is the same as the previous, increment the run
        if curr_digit == prev_digit:
            curr_run += 1

        # This digit isn't the same as the previous, record the length of the run that just
        # finished and reset the run back to 1
        else:
            digit_runs.append(curr_run)
            curr_run = 1

        prev_digit = curr_digit

        # If this digit is less than the previous, bail because the password isn't valid
        if i > 0 and password[i - 1] > curr_digit:
            return False

    # Record the length of the run of the last unique digit in the password
    digit_runs.append(curr_run)

    # If we got here, the password is potentially valid (no decreasing digits).
    # Apply the digit run check predicate which is the final validity check
    return digit_run_check(digit_runs)


def _count_valid_passwords(lower_bound, upper_bound, digit_run_check):
    """Iterates through all passwords in the range specified in the puzzle input, counting
    how many passwords are valid for the specified digit run check."""

    num_valid_passwords = 0
    for n in range(lower_bound, upper_bound + 1):
        if _validate_password(n, digit_run_check):
            num_valid_passwords += 1

    return num_valid_passwords


@aoc_output_formatter(2019, 4, 1, "number of valid passwords")
def part_one(lower_bound, upper_bound):
    return _count_valid_passwords(lower_bound, upper_bound, has_run_of_at_least_two)


@aoc_output_formatter(2019, 4, 2, "number of valid passwords")
def part_two(lower_bound, upper_bound):
    return _count_valid_passwords(lower_bound, upper_bound, has_run_of_exactly_two)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    lower_bound, upper_bound = tuple(
        int(n) for n in get_input(input_file)[0].split("-")
    )
    part_one(lower_bound, upper_bound)
    part_two(lower_bound, upper_bound)

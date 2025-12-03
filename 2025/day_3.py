from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 3
YEAR = 2025

PART_ONE_DESCRIPTION = "total joltage for best 2 batteries in each bank"
PART_ONE_ANSWER = 17263

PART_TWO_DESCRIPTION = "total joltage for best 12 batteries in each bank"
PART_TWO_ANSWER = 170731717900423


def _highest_joltage(bank: str) -> int:
    """Return the highest possible joltage for 2 batteries in this bank.

    The "joltage" is the number formed by selecting only 2 digits from the bank,
    without changing the digits' order relative to one another.

    Ex: 12345 -> 45
    Ex: 19118 -> 98
    Ex: 76227 -> 77.
    """
    best = 0

    # For any starting digit a (except the final digit)...
    for ix, a in enumerate(bank[:-1]):
        # ...check every digit b that follows it.
        # Remember the highest integer `ab` that we find.
        for b in bank[ix + 1 :]:
            best = max(best, int(f"{a}{b}"))

    return best


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return sum(_highest_joltage(battery_bank) for battery_bank in raw_input)


def _highest_joltage_v2(bat: str) -> int:
    """Return the highest possible joltage for 12 batteries in this bank.

    The "joltage" is the number formed by selecting 12 digits from the bank,
    without changing the digits' order relative to one another.
    """
    digits: list[str] = []

    remaining_bat = list(bat)

    # We need to leave at least `s` digits remaining after digit selection.
    # Our first digit selection must leave at least 11 digits following.
    # The next digit selection must leave at least 10 digits following, etc.
    #
    # For each loop, choose the largest digit in the available options that leave
    # enough remaining digits in the next loop, and then trim the "remaining battery bank"
    # down to every battery that follows the digit we just chose.
    for size in reversed(range(1, 12)):
        # Choose the largest digit from the front of the bank that leaves at least
        # `size` digits remaining afterwards.
        best_digit = max(int(n) for n in remaining_bat[: -1 * size])
        best_digit_str = str(best_digit)

        digits.append(best_digit_str)

        # The next digit chosen must selected from only the batteries that
        # follow the one we just chose.
        remaining_bat = remaining_bat[remaining_bat.index(best_digit_str) + 1 :]

    # When we reach here, we don't need to leave anymore digits remaining since
    # it's the final battery being chosen. Choose the largest of whatever's left.
    digits.append(str(max(int(n) for n in remaining_bat)))

    return int("".join(digits))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    return sum(_highest_joltage_v2(battery_bank) for battery_bank in raw_input)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

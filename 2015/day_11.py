from collections.abc import Generator
from string import ascii_lowercase

from util.decorators import aoc_output_formatter

DAY = 11
YEAR = 2015

PART_ONE_DESCRIPTION = "Santa's next password"
PART_ONE_ANSWER = "vzbxxyzz"

PART_TWO_DESCRIPTION = "Santa's password after that"
PART_TWO_ANSWER = "vzcaabcc"


def _is_valid_password(password: str) -> bool:
    """Check if the password is valid."""

    # If the password contains i, o, or l, it's not valid
    for forbidden_char in "iol":
        if forbidden_char in password:
            return False

    # The password must contain at least one increasing straight of 3 letters (abc, bcd, xyz)
    found_letter_straight = False

    for i in range(len(password) - 2):
        if password[i : i + 3] in ascii_lowercase:
            found_letter_straight = True
            break

    if not found_letter_straight:
        return False

    # The password must contain at least two different, non-overlapping letter pairs (aa, cc)
    num_letter_pairs = 0
    index_generator = (n for n in range(len(password) - 1))
    for i in index_generator:
        if password[i] == password[i + 1]:
            num_letter_pairs += 1
            try:
                # Skip the next index, since we can't have overlapping letter pairs
                next(index_generator)
            except StopIteration:
                break

    return num_letter_pairs >= 2


def _increment_password(password: str) -> str:
    """Increment the password.

    Change the last letter to the following letter in the alphabet, and if the any letter
    goes from `z` back to `a`, additionally increment the next letter.
    """

    # Convert the password into a list of indices of those letters, in reverse order. The order
    # is reversed so we can start with incrementing the "first" character and then move on
    index_buffer = list(reversed([ascii_lowercase.index(c) for c in password]))

    # Starting at the first char in the reversed password, so the last char in the password...
    for i, char_index in enumerate(index_buffer):
        # Increment the index of the password character mod 26 (so we stay in the range a-z)
        # an update the character's index in the password
        index_buffer[i] = (char_index + 1) % 26

        # If the current "new index" is not 0, then we didn't circle back to a from z, so we can
        # just break and return. If we did overflow from z back to a, we need to stay in this
        # loop so we can increment the next character
        if index_buffer[i] != 0:
            break

    return "".join(ascii_lowercase[i] for i in reversed(index_buffer))


def _password_generator(password: str) -> Generator[str]:
    """Endless generator of valid Santa passwords."""

    while True:
        password = _increment_password(password)
        if _is_valid_password(password):
            yield password


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(previous_password: str) -> str:
    return next(_password_generator(previous_password))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(previous_password: str) -> str:
    return next(_password_generator(previous_password))


def run(_: str) -> None:
    part_two(part_one("vzbxkghb"))

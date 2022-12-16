from string import ascii_lowercase

from util.decorators import aoc_output_formatter

DAY = 11
YEAR = 2015

PART_ONE_DESCRIPTION = "Santa's next password"
PART_ONE_ANSWER = "vzbxxyzz"

PART_TWO_DESCRIPTION = "Santa's password after that"
PART_TWO_ANSWER = "vzcaabcc"


# Hold all adjacent letter triplets from ascii_lowercase in a set, for faster lookup than `in`
LETTER_STRAIGHT_TRIPLES = set(
    ascii_lowercase[i : i + 3] for i in range(len(ascii_lowercase) - 2)
)


def _is_valid_password(password):
    """Checks if the password is valid."""

    # If the password contains i, o, or l, it's not valid
    for forbidden_char in "iol":
        if forbidden_char in password:
            return False

    # The password must contain at least one increasing straight of 3 letters (abc, bcd, xyz)
    found_letter_straight = False

    for i in range(len(password) - 2):
        if password[i : i + 3] in LETTER_STRAIGHT_TRIPLES:
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


def _increment_password(password):
    """Increments the password by changing the last letter to the following letter in the
    alphabet, and if the any letter goes from `z` back to `a`, additionally increment the
    next."""

    # Convert the password into a list of indices of those letters, in reverse order. The order
    # is reversed so we can start with incrementing the "first" character and then move on
    index_buffer = list(reversed([ascii_lowercase.index(c) for c in password]))

    # Starting at the first char in the reversed password, so the last char in the password...
    for i, char_index in enumerate(index_buffer):
        # Increment the index of the password character mod 26 (so we stay in the range a-z)
        # an update the character's index in the password
        char_index = (char_index + 1) % 26
        index_buffer[i] = char_index

        # If the current "new index" is not 0, then we didn't circle back to a from z, so we can
        # just break and return. If we did overflow from z back to a, we need to stay in this
        # loop so we can increment the next character
        if char_index != 0:
            break

    return "".join(ascii_lowercase[i] for i in reversed(index_buffer))


def _password_generator(password):
    """And endless generator of valid Santa passwords, starting with the next password after the
    provided one."""

    while True:
        password = _increment_password(password)
        if _is_valid_password(password):
            yield password


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(password_generator):
    return next(password_generator)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(password_generator):
    return next(password_generator)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    password_generator = _password_generator("vzbxkghb")

    part_one(password_generator)
    part_two(password_generator)

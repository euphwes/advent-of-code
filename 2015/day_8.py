from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def __count_decoded(s):
    """ Counts the number of decoded characters in an encoded string. """

    count = 0

    # Strip the framing quotes, form an iterable over the stuff inside. Capture the iterable in a
    # named variable so we can `next(...)` it later to skip characters
    s = s[1:-1]
    s_iterable = enumerate(s)

    for i, char in s_iterable:

        count += 1

        # If this character is not a backslash, it's just the literal character.
        if char != '\\':
            continue

        # If it's \xAB, we need to skip over the next three escape sequence characters.
        if s[i+1] == 'x':
            for _ in range(3):
                next(s_iterable)

        # Otherwise it must be either \\ or \", the only other two escape sequences, so we can
        # just skip the next character.
        else:
            next(s_iterable)

    return count


def __count_encoded(s):
    """ Counts the number of characters in the encodes representation of the supplied string. """

    # Start with 2 for the framing quotes, then add 2 for literal " or \, and 1 for everything else
    return 2 + sum(2 if c in ('\\', '\"') else 1 for c in s)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 8, 1, 'answer', assert_answer=1333)
def part_one(lines):
    return sum(len(s) for s in lines) - sum(__count_decoded(s) for s in lines)


@aoc_output_formatter(2015, 8, 2, 'answer', assert_answer=2046)
def part_two(lines):
     return sum(__count_encoded(s) for s in lines) - sum(len(s) for s in lines)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    lines = get_input(input_file)

    part_one(lines)
    part_two(lines)

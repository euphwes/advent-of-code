from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable, int_stream, bidirectional_range
from util.structures import get_neighbors_of

#---------------------------------------------------------------------------------------------------

def _reduce_line(line):
    """ Remove all matched pairs of brackets until either an empty string remains, or the string
    only contains unpaired brackets. """

    last_len = len(line)
    while True:
        for x in ['()', '[]', '{}', '<>']:
            while x in line:
                line = line.replace(x, '')
        new_len = len(line)
        if new_len == last_len:
            return line
        last_len = new_len


@aoc_output_formatter(2021, 10, 1, 'syntax score')
def part_one(lines):
    syntax_score = 0
    for line in lines:
        # Reduce each line, and only considering closing bracket characters.
        # If there are any closing brackets, the line is corrupt.
        # If there are no closing brackets, the line is incomplete. Discard these for now.
        r = [c for c in _reduce_line(line) if c in '>})]']
        if not r:
            continue

        # Score the syntax error by assigning points to the first incorrect closing bracket.
        syntax_score += {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }[r[0]]
    return syntax_score


def _score_autocomplete(line):
    autocomplete_score = 0
    for c in line:
        autocomplete_score *= 5
        autocomplete_score += {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }[c]
    return autocomplete_score


bracket_map = {
    '{' : '}',
    '<' : '>',
    '[' : ']',
    '(' : ')',
}


@aoc_output_formatter(2021, 10, 2, 'middle autocomplete score')
def part_two(lines):
    incomplete = list()
    for line in lines:
        # Reduce each line, and only considering closing bracket characters.
        # If there are any closing brackets, the line is corrupt. Discard these.
        # If there are closing brackets, the line is incomplete. Save these to operate on.
        r = [c for c in _reduce_line(line) if c in '>})]']
        if not r:
            incomplete.append(line)

    # For each incomplete line, determine the necessary closing brackets to complete the sequence.
    how_to_complete = list()
    for line in incomplete:
        reduced = _reduce_line(line)
        complete = ''
        for c in reduced[::-1]:
            complete += bracket_map[c]
        how_to_complete.append(complete)

    # Score each autocomplete sequence and return the middle one.
    scores = [_score_autocomplete(line) for line in how_to_complete]
    scores.sort()

    a = len(scores)
    b = a // 2

    return scores[b]

#---------------------------------------------------------------------------------------------------

def run(input_file):

    lines = [line for line in get_input(input_file)]

    part_one(lines[:])
    part_two(lines[:])

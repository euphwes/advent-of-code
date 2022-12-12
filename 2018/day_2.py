from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import Counter
from itertools import combinations

DAY  = 2
YEAR = 2018

PART_ONE_DESCRIPTION = 'checksum of box IDs'
PART_ONE_ANSWER = 5976

PART_TWO_DESCRIPTION = 'letters common between two correct box IDs'
PART_TWO_ANSWER = 'xretqmmonskvzupalfiwhcfdb'

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(boxes):

    words_with_doubles = 0
    words_with_triples = 0

    # For every box ID, count the number of times its letters appear
    for box_id in boxes:
        letter_counts = Counter(box_id)

        # For a box where any letter appears exactly 2 times or 3 times, update the respective count
        if any(count == 2 for count in letter_counts.values()):
            words_with_doubles += 1

        if any(count == 3 for count in letter_counts.values()):
            words_with_triples += 1

    return words_with_doubles * words_with_triples


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(boxes):

    # All the boxes are the same size
    box_id_size = len(boxes[0])

    for b1, b2 in combinations(boxes, 2):

        # For each pair of boxes, count how many letters differ at each index.
        differing_count = 0
        for i in range(box_id_size):
            if b1[i] != b2[i]:
                # Remember the ix because we'll need it later.
                differing_ix = i
                differing_count += 1
                # We're looking for a pair of boxes with exactly 1 differing letter. If we've already
                # identified more, we can just skip to the next pair of boxes.
                if differing_count > 1:
                    break

        if differing_count == 1:
            return b1[:differing_ix] + b1[differing_ix+1:]

#---------------------------------------------------------------------------------------------------

def run(input_file):

    boxes = get_input(input_file)

    part_one(boxes)
    part_two(boxes)

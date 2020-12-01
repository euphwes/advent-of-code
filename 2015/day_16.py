from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from itertools import product

#---------------------------------------------------------------------------------------------------

def __parse_mfcsam_output(output):
    """ Parses the output from the MFCSAM analyzer and returns a map containing the number of each
    type of thing it found. """

    values = dict()

    for line in output.split('\n'):
        line = line.strip()
        thing, amount = line.split(': ')
        values[thing] = int(amount)

    print(values)
    return values


def __parse_aunt_sue(line):
    """ Parses a description of what the elf remembers about this particular Aunt Sue. """

    # ex: `Sue 1: goldfish: 9, cars: 0, samoyeds: 9`
    sue = dict()

    # Extract the number of this Aunt Sue from the first portion, and then separate the rest
    first_colon_ix = line.index(':')
    number, rest = int(line[:first_colon_ix].replace('Sue ','')), line[first_colon_ix + 2:]
    sue['number'] = number

    # For the remainder, extract the property and value for the things about this Aunt Sue
    for token in rest.split(', '):
        attr, amount = token.split(': ')
        sue[attr] = int(amount)

    return sue

# Save some comparators (equal, less than, greater than) so we can shove them in a map for the
# property we're checking for each Aunt Sue
__eq = lambda sue, other: sue == other
__lt = lambda sue, other: sue < other
__gt = lambda sue, other: sue > other

# The correct comparators
__mfcsam_comparators = {
    'cats':        __gt,
    'trees':       __gt,
    'goldfish':    __lt,
    'pomeranians': __lt
}

def __check_aunt_sues(sue_list, attributes, comparator_map):
    """ Check each Aunt Sue against the attributes from the MFCSAM to see which Sue is a match. """

    for sue in sue_list:
        # Start by assuming this Sue is the correct one
        is_correct_sue = True

        # Iterate each attribute in the MFCSAM output
        for attr, number in attributes.items():

            # If we don't remember about this attribute for this Sue, then skip it
            if attr not in sue.keys():
                continue

            # If we do remember, check if matches this Aunt Sue.
            # If it doesn't, we know this isn't the right Sue, and we skip checking the other attrs
            # Use the supplied comparator between what you remember about this Sue and the attribute
            # we're checking.

            # Get the right comparator for this attribute, falling back on checking equality
            comparator = comparator_map.get(attr, __eq)

            if not comparator(sue[attr], number):
                is_correct_sue = False
                break

        # If we didn't otherwise indicate this Sue was the wrong one, it must be right!
        if is_correct_sue:
            return sue['number']

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 16, 1, "Aunt Sue #")
def part_one(sue_list, attributes):
    return __check_aunt_sues(sue_list, attributes, dict())


@aoc_output_formatter(2015, 16, 2, "Correct Aunt Sue #")
def part_two(sue_list, attributes):
    return __check_aunt_sues(sue_list, attributes, __mfcsam_comparators)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    # Parse Aunt Sue list from the input file
    aunt_sue_list = [__parse_aunt_sue(line[0]) for line in get_tokenized_input(input_file, '\n')]

    properties = __parse_mfcsam_output("""children: 3
                      cats: 7
                      samoyeds: 2
                      pomeranians: 3
                      akitas: 0
                      vizslas: 0
                      goldfish: 5
                      trees: 3
                      cars: 2
                      perfumes: 1""")

    part_one(aunt_sue_list, properties)
    part_two(aunt_sue_list, properties)

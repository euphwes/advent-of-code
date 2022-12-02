from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

from random import shuffle

#---------------------------------------------------------------------------------------------------

def __parse(input_lines):
    """ Parses the input file to return a list of chemical reactions which are possible, and the
    target medicine molecule. """

    reactions = list()

    for line in [line for line in input_lines if line]:
        if ' => ' in line:
            reactions.append(line.split(' => '))
        else:
            medicine_molecule = line

    return reactions, medicine_molecule


def all_indices_of(string, target):
    """ Returns a generator which yields all indices where the target appears in the provided
    string. """

    target_length = len(target)
    for i in range(len(string) - target_length + 1):
        if string[i : i + target_length] == target:
            yield i

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 19, 1, 'number of distinct molecules after 1 replacement', assert_answer=576)
def part_one(reactions, medicine_molecule):
    new_molecules = set()
    for start, finish in reactions:
        for i in all_indices_of(medicine_molecule, start):
            molecule = medicine_molecule[:i] + finish + medicine_molecule[i + len(start):]
            new_molecules.add(molecule)

    return len(new_molecules)


@aoc_output_formatter(2015, 19, 2, 'minimum number of replacements to create medicine', assert_answer=207)
def part_two(reactions, medicine_molecule):

    # Figure out the reverse problem; how many steps to go from the medicine molecule to the
    # starting molecule.
    target_molecule = 'e'
    molecule = medicine_molecule

    replacements = 0

    while molecule != target_molecule:
        # Holds how many replacements have been made since the last pass through the reactions
        replacements_this_pass = 0

        # Iterate over the possible reactions in order, and while the reaction result is still in
        # the molecule, do the opposite reaction to shorten the molecule towards the goal.
        for start, finish in reactions:
            while finish in molecule:
                i = molecule.index(finish)
                molecule = molecule[:i] + start + molecule[i + len(finish):]
                replacements += 1
                replacements_this_pass += 1

        # If we've gone through every reaction at least once and then have made another pass through
        # without any replacements being made, we're not going to make any more progress. Reset the
        # the total replacements count, reset the molecule back the complete medicine molecule, and
        # randomly shuffle the order of the reactions. Next time through, doing the replacements in
        # a different order will yield a different "reduction path" and maybe that one will work.
        if not replacements_this_pass:
            shuffle(reactions)
            molecule = medicine_molecule
            replacements = 0

    return replacements

#---------------------------------------------------------------------------------------------------

def run(input_file):

    reactions, medicine_molecule = __parse(get_input(input_file))

    part_one(reactions, medicine_molecule)
    part_two(reactions, medicine_molecule)

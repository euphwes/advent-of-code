from random import shuffle

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 19
YEAR = 2015

PART_ONE_DESCRIPTION = "number of distinct molecules after 1 replacement"
PART_ONE_ANSWER = 576

PART_TWO_DESCRIPTION = "minimum number of replacements to create medicine"
PART_TWO_ANSWER = 207


def _parse(input_lines):
    """Parses the input file to return a list of chemical reactions which are possible, and the
    target medicine molecule."""

    reactions = list()
    medicine_molecule = None

    for line in [line for line in input_lines if line]:
        if " => " in line:
            reactions.append(line.split(" => "))
        else:
            medicine_molecule = line

    return reactions, medicine_molecule


def _all_indices_of(string, target):
    """Returns a generator which yields all indices where the target appears in the provided
    string."""

    target_length = len(target)
    for i in range(len(string) - target_length + 1):
        if string[i : i + target_length] == target:
            yield i


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(reactions, medicine_molecule):
    new_molecules = set()
    for start, finish in reactions:
        for i in _all_indices_of(medicine_molecule, start):
            molecule = (
                medicine_molecule[:i] + finish + medicine_molecule[i + len(start) :]
            )
            new_molecules.add(molecule)

    return len(new_molecules)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(reactions, medicine_molecule):

    # Figure out the reverse problem; how many steps to go from the medicine molecule to the
    # starting molecule.
    target_molecule = "e"
    molecule = medicine_molecule

    replacements = 0

    while molecule != target_molecule:
        # Holds how many replacements have been made since the last pass through the reactions
        replacements_this_pass = 0

        # Iterate over the possible reactions in order, and while the reaction result is still
        # in the molecule, do the opposite reaction to shorten the molecule towards the goal.
        for start, finish in reactions:
            while finish in molecule:
                i = molecule.index(finish)
                molecule = molecule[:i] + start + molecule[i + len(finish) :]
                replacements += 1
                replacements_this_pass += 1

        # If we've gone through every reaction at least once and then have made another pass
        # through without any replacements being made, we're not going to make any more
        # progress. Reset the the total replacements count, reset the molecule back the complete
        # medicine molecule, and randomly shuffle the order of the reactions. Next time through,
        # doing the replacements in a different order will yield a different "reduction path"
        # and maybe that one will work.
        # (HACK ALERT yes I know)
        if not replacements_this_pass:
            shuffle(reactions)
            molecule = medicine_molecule
            replacements = 0

    return replacements


# ----------------------------------------------------------------------------------------------


def run(input_file):

    reactions, medicine_molecule = _parse(get_input(input_file))

    part_one(reactions, medicine_molecule)
    part_two(reactions, medicine_molecule)

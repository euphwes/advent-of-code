from functools import reduce
from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 24
YEAR = 2015

PART_ONE_DESCRIPTION = "ideal quantum entanglement of 1st of 3 groups of packages"
PART_ONE_ANSWER = 11266889531

PART_TWO_DESCRIPTION = "ideal quantum entanglement of 1st of 4 groups of packages"
PART_TWO_ANSWER = 77387711


def _quantum_entanglement(group):
    return reduce(lambda x, y: x * y, group)


def _get_smallest_package_groups(packages, group_target_weight):
    """Determines the smallest number of packages that can yield the target weight, and then
    returns all groups of that size."""

    smallest_groups = list()
    for n in range(2, len(packages) + 1):
        for combo in combinations(packages, n):
            if sum(combo) == group_target_weight:
                smallest_groups.append(combo)
        if smallest_groups:
            return smallest_groups

    # Shouldn't reach here, but return the list anyway so Intellisense can correctly infer
    # this will always return a list.
    return smallest_groups


def _get_qe_of_ideal_first_package_group(packages, num_package_groups):
    """Returns the quantum entanglement of the ideal first group of packages."""

    # figure out the target weight of each group of packages (total weight over number groups)
    total_weight = sum(packages)
    group_target_weight = total_weight / num_package_groups

    # find all groups of packages that sum to the target weight that are the smallest number of
    # individual packages
    smallest_groups = _get_smallest_package_groups(packages, group_target_weight)

    # sort by quantum entanglement
    smallest_groups.sort(key=_quantum_entanglement)

    # return the quantum entanglement of the first group of packages (smallest qe)
    return _quantum_entanglement(smallest_groups[0])


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(packages, num_package_groups):
    return _get_qe_of_ideal_first_package_group(packages, num_package_groups)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(packages, num_package_groups):
    return _get_qe_of_ideal_first_package_group(packages, num_package_groups)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    packages = [int(line) for line in get_input(input_file)]

    part_one(packages, 3)
    part_two(packages, 4)

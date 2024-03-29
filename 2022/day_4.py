from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 4
YEAR = 2022

PART_ONE_DESCRIPTION = "count of elf pairs where assignments fully contain the other"
PART_ONE_ANSWER = 567

PART_TWO_DESCRIPTION = "count of elf pairs where assignments overlap"
PART_TWO_ANSWER = 907


def _get_elf_sections(elf_assignment):
    """Gets a set of assigned section numbers for the provided elf assignment from the input."""

    start, end = (int(endcap) for endcap in elf_assignment.split("-"))
    return set(range(start, end + 1))


def _get_assignments(elf_pair):
    """Returns a tuple of sets of assigned sections for the provided elf pair."""

    elf_1, elf_2 = elf_pair.split(",")
    return _get_elf_sections(elf_1), _get_elf_sections(elf_2)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(elf_pairs):

    matches = 0

    for pair in elf_pairs:
        # Get sets of numbers representing assigned sections for each elf.
        section_1, section_2 = _get_assignments(pair)

        # If any section fully contains the other, then `contained_section - containing_section`
        # will evaluate to an empty set.
        if section_1 - section_2 == set() or section_2 - section_1 == set():
            matches += 1

    return matches


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(elf_pairs):

    matches = 0

    for pair in elf_pairs:
        # Get sets of numbers representing assigned sections for each elf.
        section_1, section_2 = _get_assignments(pair)

        # If the intersection of both sets contains any shared elements, the assignments overlap.
        if section_1 & section_2:
            matches += 1

    return matches


# ----------------------------------------------------------------------------------------------


def run(input_file):

    elf_pairs = get_input(input_file)

    part_one(elf_pairs)
    part_two(elf_pairs)

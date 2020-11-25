from util.decorators import aoc_output_formatter
from util.input import get_input

from json import loads

#---------------------------------------------------------------------------------------------------

def __evaluate_document_sum(document, ignore_red=False):
    """ Parses a JSON document and returns the sum of all numerical values in it. """

    # A string is always zero-valued.
    if type(document) == str:
        return 0

    # Just return the integer itself, if it's an integer.
    if type(document) == int:
        return document

    # If we're inspecting an object, sum all of its values.
    if type(document) == dict:
        if ignore_red and "red" in document.values():
            return 0
        return sum(__evaluate_document_sum(item, ignore_red) for item in document.values())

    # If we're inspecting a list, sum of all its values.
    if type(document) == list:
        return sum(__evaluate_document_sum(item, ignore_red) for item in document)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 12, 1, "Accounting document sum")
def part_one(document):
    return __evaluate_document_sum(document)


@aoc_output_formatter(2015, 12, 2, "Accounting document sum, ignoring red objects")
def part_two(document):
    return __evaluate_document_sum(document, ignore_red=True)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    document = loads(get_input(input_file)[0])

    part_one(document)
    part_two(document)

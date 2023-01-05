from copy import copy

from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

DAY = 8
YEAR = 2018

PART_ONE_DESCRIPTION = "sum of all metadata entries"
PART_ONE_ANSWER = 35852

PART_TWO_DESCRIPTION = "value of the root node"
PART_TWO_ANSWER = 33422


def _get_length_of_next_child(numbers_starting_at_child):
    """Given a chunk of numbers that is NOT a full node (including header and metadata), but
    instead is just some number of children nodes back-to-back, find and return the length of
    the next child node in this list of numbers.

    For example, given the following full root node

    3 3 0 3 10 11 12 1 1 0 1 99 2 1 1 0 1 99 2 1 1 2
    A-----------------------------------------------
        B----------- C----------- D-----------
                        E-----       F-----

    the header is [3, 3], and the metadata is [1, 1, 2]
    leaving children back-to-back:

    0 3 10 11 12 1 1 0 1 99 2 1 1 0 1 99 2
    B----------- C----------- D-----------
                    E-----       F-----

    The next child is B and has a length of 5.

    If we pass in:

    1 1 0 1 99 2 1 1 0 1 99 2
    C----------- D-----------
        E-----       F-----

    The next child is C and has a length of 6 (1, 1, 0, 1, 99, 2).
    """

    numbers_copy = copy(numbers_starting_at_child)

    children_len = numbers_copy[0]
    metadata_len = numbers_copy[1]

    # So far we know it's header + metadata length
    next_child_len = 2 + metadata_len

    # Scan ahead out of the header into the first grandchild header.
    ix = 2

    for _ in range(children_len):

        # Extract the number of children and metadata entry count from this grandchild.
        gchildren_len = numbers_copy[ix]
        gmetadata_len = numbers_copy[ix + 1]

        # If the granchild has no children, its length is just 2 (headers) + its metadata count.
        if gchildren_len == 0:
            subchild_len = 2 + gmetadata_len

        # Otherwise, find the length of this grandchild by recursively calling this function
        # with the list of numbers starting at the beginning of the grandchild.
        else:
            subchild_len = _get_length_of_next_child(numbers_copy[ix:])

        # Once we know the length of the grandchild, add it to the length of the child
        next_child_len += subchild_len

        # Scan ahead by the length of the grandchild to get to the next one.
        ix += subchild_len

    return next_child_len


def _get_children_and_metadata(one_node):
    """Given a list of numbers representing a full node, return a list of its children and a
    list of its metadata entries.

    For example, given:
    3 3 0 3 10 11 12 1 1 0 1 99 2 1 1 0 1 99 2 1 1 2
    A-----------------------------------------------
        B----------- C----------- D-----------
                        E-----       F-----

    this will return:
    children = [
        [0, 3, 10, 11, 12],
        [1, 1, 0, 1, 99, 2],
        [1, 1, 0, 1, 99, 2]
    ]
    metadata = [1, 1, 2]
    """

    children = list()
    metadata = list()

    children_count = one_node.pop(0)
    metadata_count = one_node.pop(0)

    # Since `one_node` is a list of numbers representing a single node, regardless of how many
    # children this node has, all the metadata will be the digits at the end of the numbers.
    for _ in range(metadata_count):
        metadata.append(one_node.pop(-1))

    # Now we've stripped the header and the metadata, what's left are some numbers representing
    # the N child nodes of this parent node. Break them into the correct chunks for each child.

    # If no children, we're done.
    if children_count == 0:
        return children, metadata

    remainder = one_node

    # If there are children...
    for _ in range(children_count):

        # Find the length of the next child from the remainder (just the children portion of
        # this node)
        child_len = _get_length_of_next_child(remainder)

        # Extract that child from the remainder and add it to the list of children
        children.append(remainder[:child_len])

        # Remove that child from the remainder
        remainder = remainder[child_len:]

    return children, metadata


def _get_value_of_node(children, metadata):
    """Returns the value of a node, given its children and its metadata entries."""

    # If this node has no children, its value is the sum of its metadata entries.
    if not children:
        return sum(metadata)

    # Otherwise the value of the node is the sum of all its children nodes' values, as
    # indexed by its metadata entries.
    #
    # Example:
    # children: [
    #     <node with value 5>,
    #     <node with value 7>,
    # ]
    # metadata: [1, 2, 3, 2]
    #
    # The stuff in metadata references children by its 1-indexed position. Metadata value 1
    # refers to the 1st child. Metadata value 2 refers to the 2nd child. Metadata value 3 refers
    # to a 3rd child which doesn't exist.
    #
    # So the value of this node is
    # 5 + 7 + (doesn't exist, so 0) + 7 = 19
    else:
        node_value = 0

        for metadata_value in metadata:
            try:
                # We need to copy the child node here, because _get_children_and_metadata
                # mutates the list of numbers by popping values off, and we might reference this
                # same child again later by a duplicate metadata value.
                child_node = copy(children[metadata_value - 1])

                grandchildren, child_metadata = _get_children_and_metadata(child_node)
                node_value += _get_value_of_node(grandchildren, child_metadata)

            except IndexError:
                pass

        return node_value


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(filesystem):

    metadata = list()

    nodes = list()
    nodes.append(filesystem)

    while nodes:
        node = nodes.pop(0)
        children, metadata_entries = _get_children_and_metadata(copy(node))

        nodes.extend(children)
        metadata.extend(metadata_entries)

    return sum(metadata)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(filesystem):

    return _get_value_of_node(*_get_children_and_metadata(filesystem))


# ----------------------------------------------------------------------------------------------


def run(input_file):

    filesystem = get_tokenized_input(input_file, " ", transform=int)[0]
    part_one(filesystem)

    filesystem = get_tokenized_input(input_file, " ", transform=int)[0]
    part_two(filesystem)

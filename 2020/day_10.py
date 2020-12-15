from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict
from math import prod as product

#---------------------------------------------------------------------------------------------------

def __next_connectors(prev_conn, connectors):
    """ Returns a list of options for the next connector, given the previous connector. Valid next
    connectors are between 1 and 3 jolts higher than the previous connector. """

    return [i for i in range(prev_conn + 1, prev_conn + 4) if i in connectors]


def __get_paths(prev_conn, connectors):
    """ Returns a list of all paths through the connectors starting from the supplied connector. """

    # If no previous connector was specified, we start with the first in the list. Otherwise we
    # establish which connectors are valid options for the next connector in the path.
    if prev_conn is None:
        path_options = [connectors[0]]
    else:
        path_options = __next_connectors(prev_conn, connectors)

    paths = list()

    # For each potential next connector...
    for next_conn in path_options:

        # ... if there are more paths continuing on from that connector, append each of those paths
        # to the chosen next connector, and all of those are new paths are paths from the prev conn
        options = __get_paths(next_conn, connectors)
        if options:
            for option in options:
                paths.append([next_conn] + option)

        # ... if there are no more paths continuing on from that connector, it's the last one in
        # the path.
        else:
            paths.append([next_conn])

    return paths


def __remove_single_path_runs(connectors):
    """ Identifies all path options for each connector, and finds all runs where connectors only
    have a single additional connector to connect. Removes those single-path runs and returns the
    remaining connectors as groups which have multiple paths through them.

    Ex. [0, 1, 4, 5, 6, 7, 10, 11, 12, 15]

    Connector    Potential Paths
    0:           [1]
    1:           [4]
    4:           [5, 6, 7]
    5:           [6, 7]
    6:           [7]
    7:           [10]
    10:          [11, 12]
    11:          [12]
    12:          [15]

    returns [
        [4, 5, 6, 7],
        [10, 11, 12]
    ]

    because [4, 5, 6, 7] has multiple paths from 4 to 7, and [10, 11, 12] has multiple paths from
    10 to 12. The remaining connectors only have a single path through them and do not add
    complexity to the problem. """

    # Pair each connector with its path options
    connector_paths = [(n, __next_connectors(n, connectors)) for n in connectors]

    current_group = list()
    connector_groups = list()

    # Iterate each connector and its paths
    for conn, paths in connector_paths:
        # If this connector has more than one path forward, it's part of a group of connectors
        # with multiple paths. Append this connector, and all of its options, to the current group.
        if len(paths) > 1:
            current_group.append(conn)
            current_group.extend(paths)
            continue
        # If this connector has only 1 path forward, see if we're currently tracking a group.
        # If not, this connector is part of a run of single-path connectors and we can skip it.
        if not current_group:
            continue
        # If this connector has only 1 path forward and we're currently tracking a group, this is
        # the final connector in a group of connectors with multiple paths. Clean up the group by
        # removing duplicates, ensure it's sorted, and add the group to the list of connector groups.
        current_group = sorted(list(set(current_group)))
        connector_groups.append(current_group)
        # Clear the current group so we can start tracking the next one.
        current_group = list()

    return connector_groups

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 10, 1, "product of num of 1-jolt and 3-jolt differences")
def part_one(connectors):
    diffs = defaultdict(int)
    for i in range(len(connectors)-1):
        diffs[connectors[i+1] - connectors[i]] += 1
    return diffs[1] * diffs[3]


@aoc_output_formatter(2020, 10, 2, 'distinct valid arrangements of connectors')
def part_two(all_connectors):

    # Chunk the connectors into discrete groups which have multiple paths running through them,
    # removing all connector runs with only 1 path. For each smaller group of connectors with
    # multiple paths through, evaluate those paths and count them. The product of number of paths
    # through each group is the total number of paths through all the connectors

    connector_groups = __remove_single_path_runs(all_connectors)
    paths_through_groups = [len(__get_paths(None, group)) for group in connector_groups]

    return product(paths_through_groups)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    connectors = [int(n) for n in get_input(input_file)]

    # The power supply is 0 jolts. Your device has a joltage rating 3 higher than the highest-rated
    # connector you have. Add 0 and max+3 to model the supply and device as connectors.
    connectors.append(0)
    connectors.append(max(connectors)+3)

    connectors.sort()

    part_one(connectors)
    part_two(connectors)

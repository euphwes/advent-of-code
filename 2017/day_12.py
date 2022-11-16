from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _map_pipes(pipes):
    """ Build and return a map where each program is represented in a key, and the value is a list
    of all other programs directly connected to the key program by a pipe.

    Ex: pipes =
    19 <-> 404, 1524, 1539, 1941
    30 <-> 355, 467, 1605

    returns
    {
        19: [404, 1524, 1539, 1941],
        30: [355, 467, 1605]
    }
    """

    pipes_map = dict()
    for pipe_mapping in pipes:
        source, targets = pipe_mapping.split(' <-> ')
        pipes_map[int(source)] = [int(target) for target in targets.split(', ')]

    return pipes_map


def _get_group_containing(target_program, pipes_map):
    """ Returns a set of all programs in the group specified by the target_program, where a group is
    any program that can be reached via pipes either directly or indirectly. """

    # Do this as a sort of breadth-first search. Start the target program in the queue, and maintain
    # a list of all programs which have been visited.
    queue = [target_program]
    visited = set()

    while queue:
        # Pop the first element from the queue and set it as visited (it's in the group).
        source_program = queue.pop(0)
        visited.add(source_program)

        # For every program this is connected to by pipe...
        for target_program in pipes_map[source_program]:
            # If we haven't already visited it (via some other pipe path), add it to the queue
            # of programs to visit.
            if target_program not in visited:
                queue.append(target_program)

    return visited


@aoc_output_formatter(2017, 12, 1, 'size of group containing program 0')
def part_one(pipes):
    pipes_map = _map_pipes(pipes)
    return len(_get_group_containing(0, pipes_map))


@aoc_output_formatter(2017, 12, 2, 'number of distinct groups of programs')
def part_two(pipes):
    pipes_map = _map_pipes(pipes)

    groups = set()

    # For every program in the pipe map...
    for starting_program in pipes_map.keys():
        # If we already have a group containing it, we don't need to check it again because it'll
        # just return the same group that contains it.
        if any(starting_program in group for group in groups):
            continue

        # Add the group containing this program to the set of groups.
        groups.add(frozenset(_get_group_containing(starting_program, pipes_map)))

    return len(groups)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    pipes = get_input(input_file)

    part_one(pipes)
    part_two(pipes)

from util.decorators import aoc_output_formatter
from util.input import get_input_grid_map
from util.iter import int_stream
from util.structures import get_neighbors_of_dict_based

DAY = 18
YEAR = 2018

PART_ONE_DESCRIPTION = "Lumber collection resource value after 10 minutes"
PART_ONE_ANSWER = 360720

PART_TWO_DESCRIPTION = "Lumber collection resource value after 1 billion minutes"
PART_TWO_ANSWER = 197276

TREES = "|"
GROUND = "."
LUMBERYARD = "#"


def _evolve_lumber_collection_map(lumber_collection_map):
    """The lumber collection area evolves over time, like a cellular automata. Evolve the map
    1 unit of time forward following the rules, and return the new state of map."""

    new_lumber_collection_map = dict()
    for coord, item in lumber_collection_map.items():
        x, y = coord
        neighbors = list(get_neighbors_of_dict_based(x, y, lumber_collection_map))
        num_adj_trees = len([n for n in neighbors if n == TREES])
        num_adj_lumber = len([n for n in neighbors if n == LUMBERYARD])

        # An open acre will become filled with trees if three or more adjacent acres contained
        # trees. Otherwise, nothing happens.
        if item == GROUND:
            new_lumber_collection_map[(x, y)] = GROUND
            if num_adj_trees >= 3:
                new_lumber_collection_map[(x, y)] = TREES

        # An acre filled with trees will become a lumberyard if three or more adjacent acre
        # were lumberyards. Otherwise, nothing happens.
        elif item == TREES:
            new_lumber_collection_map[(x, y)] = TREES
            if num_adj_lumber >= 3:
                new_lumber_collection_map[(x, y)] = LUMBERYARD

        # An acre containing a lumberyard will remain a lumberyard if it was adjacent to at
        # least one other lumberyard and at least one acre containing trees. Otherwise, it
        # becomes open.
        else:
            new_lumber_collection_map[(x, y)] = GROUND
            if num_adj_lumber >= 1 and num_adj_trees >= 1:
                new_lumber_collection_map[(x, y)] = LUMBERYARD

    return new_lumber_collection_map


def _get_static_repr(lumber_collection_map):
    """Return a single-line representation of the map, suitable for using as the key in a
    dictionary because it's hashable."""

    line = []
    for y in range(0, 50):
        for x in range(0, 50):
            line.append(lumber_collection_map[(x, y)])
    return "".join(line)


def _get_resource_value(lumber_collection_map):
    num_trees = sum(1 for item in lumber_collection_map.values() if item == TREES)
    num_lumber = sum(1 for item in lumber_collection_map.values() if item == LUMBERYARD)
    return num_trees * num_lumber


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(lumber_collection_map):
    for _ in range(10):
        lumber_collection_map = _evolve_lumber_collection_map(lumber_collection_map)

    return _get_resource_value(lumber_collection_map)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(lumber_collection_map):
    last_iteration = -1
    key_to_first_iteration = dict()

    # Iterate the lumber collection map until we see a state we've already seen before,
    # indicating we've entered a repeating cycle.
    for i in int_stream(start=1):
        lumber_collection_map = _evolve_lumber_collection_map(lumber_collection_map)
        key = _get_static_repr(lumber_collection_map)
        if key not in key_to_first_iteration.keys():
            key_to_first_iteration[key] = i
            continue

        # Once we've found the cycle, find out how long it is and advance the timestep as close
        # to 1 billion seconds as we can and then break out of this loop.
        cycle_size = i - key_to_first_iteration[key]
        while (i + cycle_size) < 1_000_000_000:
            i += cycle_size
        last_iteration = i
        break

    # Start at the next timestep after the the last one we visited, and continue evolving
    # the lumber collection area to 1 billion seconds.
    for _ in int_stream(start=last_iteration + 1, end=1_000_000_000):
        lumber_collection_map = _evolve_lumber_collection_map(lumber_collection_map)

    return _get_resource_value(lumber_collection_map)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    lumber_collection_map = get_input_grid_map(input_file)

    part_one(lumber_collection_map)
    part_two(lumber_collection_map)

from util.algs import manhattan_distance
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.structures import get_neighbors_of

from itertools import combinations, permutations
from heapq import heappush, heappop

#---------------------------------------------------------------------------------------------------

# Make these global variables, so we can calculate them once in part 1 and then use
# them again in part 2 without having to pass them around.
targets = None
wire_distance_map = None


def find_all_targets(maze):
    """ Iterate over the maze and find all numbered cells, which indicate a location
    of interest in the maze. Return a map of the value in that cell to its coordinates. """

    targets = dict()
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            try:
                cell = int(cell)
                targets[cell] = (x, y)
            except ValueError:
                pass
    return targets


def find_pairwise_shortest_distance(targets, maze):
    """ Build and return a map containing the shortest path between each pair of
    targets in the map. """

    wire_distance_map = dict()
    for wire1, wire2 in combinations(targets.keys(), r=2):
        path_distance = shortest_path(targets[wire1], targets[wire2], maze)
        wire_distance_map[(wire1, wire2)] = path_distance
        wire_distance_map[(wire2, wire1)] = path_distance

    return wire_distance_map


def shortest_path(start, target, maze):
    """ Returns the shortest path between the start and target coordinates in the given maze.
    Uses a heuristic-guided BFS search to determine shortest path. """

    queue = list()
    visited = set()

    heappush(queue, (0, 0, start))

    while queue:
        _, depth, current_coord = heappop(queue)

        visited.add(current_coord)

        if current_coord == target:
            return depth

        next_depth = depth + 1
        for cell, neighbor_coords in get_neighbors_of(
            current_coord[0],
            current_coord[1],
            maze,
            include_diagonals=False,
            with_coords=True
        ):
            if cell == '#' or neighbor_coords in visited:
                continue

            # Why this heuristic gives the correct answer, and others don't (like different
            # manhattan distance multiplicands, or not summing in next_depth, etc), who knows.
            heuristic = next_depth + (1.2 * manhattan_distance(neighbor_coords, target))
            heappush(queue, (heuristic, next_depth, neighbor_coords))


def shortest_trip(target_permutations, wire_distance_map):
    """ Returns the length of the shortest trip visiting all targets, checking every permutation
    of target ordering passed in. """

    shortest_trip = None
    for perm in target_permutations:
        trip = 0
        for i in range(len(perm)-1):
            trip += wire_distance_map[(perm[i], perm[i+1])]
        if shortest_trip is None:
            shortest_trip = trip
        elif trip < shortest_trip:
            shortest_trip = trip

    return shortest_trip


@aoc_output_formatter(2016, 24, 1, 'fewest steps to reach all wires')
def part_one(maze):
    global targets, wire_distance_map
    targets = find_all_targets(maze)
    wire_distance_map = find_pairwise_shortest_distance(targets, maze)

    # Find permutations of all targets except 0, and then add 0 to the start of all of them
    # since that's where we're starting from.
    targets_no_zero = [target for target in targets.keys() if target != 0]
    perms_no_zero = list(permutations(targets_no_zero, r=len(targets_no_zero)))
    perms = [[0] + list(perm) for perm in perms_no_zero]

    return shortest_trip(perms, wire_distance_map)


@aoc_output_formatter(2016, 24, 2, 'fewest steps to reach all wires and return to start')
def part_two(maze):

    # Find permutations of all targets except 0, and then add 0 to the start and end of all of them
    # since we're round-tripping all targets starting at 0.
    targets_no_zero = [target for target in targets.keys() if target != 0]
    perms_no_zero = list(permutations(targets_no_zero, r=len(targets_no_zero)))
    perms = [[0] + list(perm) + [0] for perm in perms_no_zero]

    return shortest_trip(perms, wire_distance_map)


#---------------------------------------------------------------------------------------------------

def run(input_file):

    maze = get_input(input_file)

    part_one(maze)
    part_two(maze)

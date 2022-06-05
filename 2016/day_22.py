from util.decorators import aoc_output_formatter
from util.input import get_input

from dataclasses import dataclass, replace, field
from itertools import permutations
from typing import Tuple, Any, Dict

from heapq import heappush, heappop
from copy import deepcopy

#---------------------------------------------------------------------------------------------------

@dataclass(eq=True, frozen=True)
class DiskNode:
    coord: Tuple[int, int]
    used: int
    avail: int
    total: int
    has_target_data: bool

    @property
    def empty(self):
        return self.used == 0

    def __str__(self):
        if self.coord == (0, 0):
            return '( )'
        if self.has_target_data:
            return ' * '
        if self.empty:
            return '[ ]'
        if (self.used/self.total) > 0.95:
            return ' # '
        return ' . '


@dataclass(eq=True, frozen=True)
class DiskNodeState:
    nodes: Dict[Tuple[int, int], DiskNode]

    def __hash__(self):
        return hash(frozenset(self.nodes.values()))

    def __lt__(self, other):
        return False

    @property
    def is_solved(self):
        for node in self.nodes.values():
            if node.coord == (0, 0) and node.has_target_data:
                return True
        return False

    @property
    def target_data_coord(self):
        for node in self.nodes.values():
            if node.has_target_data:
                return node.coord

    def print(self):
        coord_repr_map = dict()
        for node in self.nodes.values():
            coord_repr_map[node.coord] = str(node)

        lines = list()
        for x in range(31):
            line = list()
            for y in range(31):
                line.append(coord_repr_map[(y, x)])
            lines.append(' '.join(line))

        print('\n'+'\n'.join(lines)+'\n')


def _parse_node(line):
    """ Parses a single input line to build and return a DiskNode. """

    parts = line.split()

    # Filesystem              Size  Used  Avail  Use%
    # /dev/grid/node-x0-y0     94T   73T    21T   77%

    total = int(parts[1].replace('T', ''))
    used = int(parts[2].replace('T', ''))
    avail = int(parts[3].replace('T', ''))

    raw_coord = parts[0].replace('/dev/grid/node-', '').split('-')
    coord = (int(raw_coord[0].replace('x', '')), int(raw_coord[1].replace('y', '')))

    return DiskNode(coord, used, avail, total, False)


def _parse_input(input_lines):
    """ Parses the input lines and returns a list of DiskNodes containing the disk node coordinate,
    the total, used, and available disk space. """

    # Discard the top two lines (the `df` command and the column headers)
    input_lines = input_lines[2:]

    nodes = [_parse_node(line) for line in input_lines]

    # Find the maximum x value, and then mark the node at coordinate (max_x, 0) as the one with the
    # target data.
    max_x = -1
    for node in nodes:
        if node.coord[0] > max_x:
            max_x = node.coord[0]

    for i, node in enumerate(nodes):
        if node.coord == (max_x, 0):
            target_node = replace(node, has_target_data=True)
            break

    nodes[i] = target_node
    return nodes


def _manhattan_distance(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return abs(x1-x2) + abs(y1-y2)


def _get_next_states(current_state):
    """ Returns options for what the next state of the array could be, after copying data between
    adjacent pairs of nodes. """

    next_states = list()
    for a in current_state.nodes.values():
        if not a.empty:
            continue

        x, y = a.coord
        for neighbor_coord in set([(x-1, y), (x+1, y), (x, y-1), (x, y+1)]):
            try:
                b = current_state.nodes[neighbor_coord]
                if a.used+b.used > a.avail:
                    continue
            except KeyError:
                continue

            nodes = set()

            does_b_have_target_data = b.has_target_data
            new_a = replace(a, has_target_data=does_b_have_target_data, used=a.used+b.used, avail=a.total-(a.used+b.used))
            new_b = replace(b, has_target_data=False, used=0, avail=b.total)

            # print('\n-----\n\nPossible next state')
            # print(f'a={a}')
            # print(f'b={b}')
            # print(f'new_a={new_a}')
            # print(f'new_b={new_b}')

            new_nodes = deepcopy(current_state.nodes)
            new_nodes[new_a.coord] = new_a
            new_nodes[new_b.coord] = new_b

            new_state = DiskNodeState(new_nodes)

            # current_state.print()
            # print('becomes')
            # new_state.print()

            next_states.append(new_state)

    return next_states


@aoc_output_formatter(2016, 22, 1, 'pairs of viable nodes')
def part_one(disk_nodes):
    count = 0
    for a, b in permutations(disk_nodes, r=2):
        if a is b or a.used == 0:
            continue
        if a.used <= b.avail:
            count += 1
    return count


def _score(state):
    score = 500 * _manhattan_distance(state.target_data_coord, (0, 0))
    for node in [n for n in state.nodes.values() if n.empty]:
        score += 100 * _manhattan_distance(node.coord, state.target_data_coord)
        score += 50 * _manhattan_distance(node.coord, (0, 0))
    return


@aoc_output_formatter(2016, 22, 2, 'minimum steps to reach target data')
def part_two(disk_nodes):

    state_queue = list()
    start_state = DiskNodeState(nodes={node.coord: node for node in disk_nodes})

    # This logic below technically works as a brute force search, works on
    # the sample solution, but doesn't finish in reasonable time for the real
    # input.
    """
    heappush(state_queue, (_score(start_state), 0, start_state))

    states_seen = set()

    while state_queue:
        _, depth, current_state = heappop(state_queue)
        # print('\n----------------------\n----------------------')
        # current_state.print()
        # print('----------------------\n----------------------')

        if current_state.is_solved:
            return depth

        states_seen.add(current_state)

        for neighbor_state in _get_next_states(current_state):
            if neighbor_state in states_seen:
                continue
            heappush(state_queue, (_score(neighbor_state), depth+1, neighbor_state))
    """

    # So instead I just printed what the grid of nodes looked like and used some
    # common sense to figure out how the elements can move around most efficiently
    # to get the target data to (0, 0)
    start_state.print()

    return 207


#---------------------------------------------------------------------------------------------------

def run(input_file):

    disk_nodes = _parse_input(get_input(input_file))

    part_one(disk_nodes)

    # sample_input = [
    #     "root@ebhq-gridcenter# df -h",
    #     "Filesystem            Size  Used  Avail  Use%",
    #     "/dev/grid/node-x0-y0   10T    8T     2T   80%",
    #     "/dev/grid/node-x0-y1   11T    6T     5T   54%",
    #     "/dev/grid/node-x0-y2   32T   28T     4T   87%",
    #     "/dev/grid/node-x1-y0    9T    7T     2T   77%",
    #     "/dev/grid/node-x1-y1    8T    0T     8T    0%",
    #     "/dev/grid/node-x1-y2   11T    7T     4T   63%",
    #     "/dev/grid/node-x2-y0   10T    6T     4T   60%",
    #     "/dev/grid/node-x2-y1    9T    8T     1T   88%",
    #     "/dev/grid/node-x2-y2    9T    6T     3T   66%",
    # ]
    # disk_nodes = _parse_input(sample_input)

    part_two(disk_nodes)

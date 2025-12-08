from functools import cache

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 7
YEAR = 2025

PART_ONE_DESCRIPTION = "number of times the tachyon beam will split"
PART_ONE_ANSWER = 1687

PART_TWO_DESCRIPTION = "number of timelines for a single tachyon particle"
PART_TWO_ANSWER = 390684413472684


Coord = tuple[int, int]


def _parse_grid(raw_input: list[str]) -> dict[Coord, str]:
    field = {}

    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            field[(x, y)] = char

    return field


def _find_splitter_coords(grid: dict[Coord, str]) -> set[Coord]:
    """Return a set of coords identifying all *accessible* splitters in the grid."""

    # Get coords for every single ^ character in the grid.
    splitters = {coord for coord, item in grid.items() if item == "^"}

    # Identify splitters which are inaccessible
    inaccessible_splitters = set()

    for x, y in splitters:
        # Go straight up from the splitter we're checking.
        while y > 0:
            y -= 1

            # If this spot above the splitter is immediately left or right of another
            # another splitter, the beam can reach this splitter so it's accessible.
            #
            # Ex:
            #    ..|^|..
            #    ..|.|..
            #    ..|.^..   <- this splitter is accessible because the splitter above
            #                 splits a beam onto this splitter

            if (x - 1, y) in splitters or (x + 1, y) in splitters:
                break

            # If this spot is itself another splitter, the splitter we're checking is
            # not accessible.
            #
            # Ex:
            #    ..|^|..
            #    ..|.|..
            #    ..|^|..   <- this splitter is hidden by the one above it

            if (x, y) in splitters:
                inaccessible_splitters.add((x, y))
                break

    # Remove inaccessible splitters because they don't play any role
    return splitters - inaccessible_splitters


def _find_node_coords(grid: dict[Coord, str], splitters: set[Coord]) -> set[Coord]:
    """Return the coords of the graph nodes that the grid implies."""

    # The "source" (S) of the tachyon beam is the first node.
    nodes = {coord for coord, item in grid.items() if item == "S"}

    # Each splitter turns the beam from 1 into 2.
    # We can think of the spaces immediately left and right of the splitter as nodes.
    for x, y in splitters:
        nodes.add((x - 1, y))
        nodes.add((x + 1, y))

    return nodes


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)
    splitters = _find_splitter_coords(grid)

    return len(splitters)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)
    splitters = _find_splitter_coords(grid)

    # We can think of this grid of splitters of tachyon beams as being a graph.
    # The beam starts at the root node (the source) and branches into 2 nodes at a splitter.
    # The beams continue, hitting more splitters (resulting in 2 more nodes) each.
    # Find coordinates of each node in the graph we're describing.
    #
    # ...S....
    # ...|....
    # ..|^|...
    # ..|.|...
    # .|^|^|..
    #
    # Can be viewed as:
    #
    # ...S....
    # ...|....
    # ..A.B...
    # ..|.|...
    # .C.D.E..
    #
    # Where A,B are children of S.
    # C,D are children of A.
    # D,E are children of B.

    nodes = _find_node_coords(grid, splitters)
    deepest_y = max(y for _, y in nodes)

    @cache
    def _count_paths(node: Coord) -> int:
        x, y = node

        # Look for children of this node by traveling directly dowards until you run
        # into a splitter, which has nodes immediately left and right of it.
        # Those nodes are children of this node.
        children = []
        while y <= deepest_y:
            y += 2
            if (x, y) in splitters and (x - 1, y) in nodes:
                children.append((x - 1, y))
            if (x, y) in splitters and (x + 1, y) in nodes:
                children.append((x + 1, y))
            if children:
                break

        # If there are no children of this node, then this node is a leaf (end) node,
        # which means it only contributes 1 path.
        if not children:
            return 1

        # Otherwise, the number of paths from this node is the sum of the number of paths
        # coming out of all of it's child nodes.
        return sum(_count_paths(child) for child in children)

    # Return the total number of paths originating out of the root node.
    root_node = min(nodes, key=lambda node: node[1])
    return _count_paths(root_node)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

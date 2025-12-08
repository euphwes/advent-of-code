from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 7
YEAR = 2025

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


Coord = tuple[int, int]


def _parse_grid(raw_input: list[str]) -> dict[Coord, str]:
    field = {}

    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            field[(x, y)] = char

    return field


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)

    splitters: set[Coord] = set()
    for coord, item in grid.items():
        if item == "^":
            splitters.add(coord)

    sources: set[Coord] = set()
    for coord, item in grid.items():
        if item == "S":
            sources.add(coord)
            break

    for x, y in splitters:
        sources.add((x - 1, y))
        sources.add((x + 1, y))

    for coord in sources:
        grid[coord] = "S"

    count = 0
    for x, y in splitters:
        found = False
        while y > 0:
            y -= 1
            if (x, y) in splitters:
                break
            if grid[(x, y)] == "S":
                found = True
                break
        if found:
            count += 1

    return count


@dataclass
class Node:
    coord: Coord
    children: list[Self]

    @property
    def num_paths(self) -> int:
        return 0


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)

    splitters: set[Coord] = set()
    for coord, item in grid.items():
        if item == "^":
            splitters.add(coord)

    sources: set[Coord] = set()
    for coord, item in grid.items():
        if item == "S":
            sources.add(coord)
            break

    for x, y in splitters:
        sources.add((x - 1, y))
        sources.add((x + 1, y))

    sources_by_y: dict[int, list[Coord]] = defaultdict(list)
    for sx, sy in sources:
        sources_by_y[sy].append((sx, sy))

    assert len(sources_by_y[0]) == 1

    find_children_queue = [
        Node(
            coord=sources_by_y[0][0],
            children=[],
        ),
    ]
    all_nodes: list[Node] = []

    while find_children_queue:
        node = find_children_queue.pop(0)

        nx, ny = node.coord
        child_y = ny + 2

        # TODO don't keep recreating child nodes

        for cx, cy in sources_by_y[child_y]:
            if cx in (nx - 1, nx + 1):
                new_node = Node(
                    coord=(cx, cy),
                    children=[],
                )
                node.children.append(new_node)
                if not new_node.children:
                    find_children_queue.append(new_node)

        all_nodes.append(node)

    for node in all_nodes:
        print(node)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

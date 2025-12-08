from collections import defaultdict
from dataclasses import dataclass
from functools import cache
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

    deepest_y = max(sources_by_y.keys())

    @cache
    def _count_paths(c: Coord) -> int:
        cx, cy = c
        if cy == deepest_y:
            return 1

        children = []

        while cy < deepest_y:
            cy += 2
            if (cx - 1, cy) in sources:
                children.append((cx - 1, cy))
                children.append((cx + 1, cy))
                break

        return sum(_count_paths(child) for child in children)

    return _count_paths(sources_by_y[sy][0])


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

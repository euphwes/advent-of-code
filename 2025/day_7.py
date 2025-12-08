from collections import defaultdict
from functools import cache

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


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)

    splitters: set[Coord] = set()
    for coord, item in grid.items():
        if item == "^":
            splitters.add(coord)

    # Remove splitters which are "inaccessible"
    splitters_to_remove = []
    for scoord in splitters:
        x, y = scoord
        while y > 0:
            y -= 1
            if (x - 1, y) in splitters:
                break
            if (x + 1, y) in splitters:
                break
            if (x, y) in splitters:
                splitters_to_remove.append(scoord)
                break

    for s in splitters_to_remove:
        splitters.remove(s)

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
            # print(f"{c} is a leaf")
            return 1

        children = []

        while cy <= deepest_y:
            cy += 2
            done = False
            if (cx, cy) in splitters and (cx - 1, cy) in sources:
                children.append((cx - 1, cy))
                done = True
            if (cx, cy) in splitters and (cx + 1, cy) in sources:
                children.append((cx + 1, cy))
                done = True
            if done:
                break

        if not children:
            return 1

        s = sum(_count_paths(child) for child in children)
        # print(f"{c} has children {children}, returning {s}")
        return s

    # for yval in sorted(sources_by_y.keys(), reverse=True):
    #     # print(f"\nEvaluating coords at y={yval}")
    #     for c in sources_by_y[yval]:
    #         count = _count_paths(c)
    #         # print(f"{c}: {count}")

    return f"{_count_paths(sources_by_y[0][0]):_}"


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

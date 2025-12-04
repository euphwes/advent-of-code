from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 4
YEAR = 2025

PART_ONE_DESCRIPTION = "number rolls of paper accessible at the start"
PART_ONE_ANSWER = 1587

PART_TWO_DESCRIPTION = "total rolls of paper that can be removed"
PART_TWO_ANSWER = 8946

Coord = tuple[int, int]

PAPER = "@"


def _parse_grid(raw_input: list[str]) -> dict[Coord, str]:
    field = {}

    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            field[(x, y)] = char

    return field


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)

    count_accessible_paper_rolls = 0

    for coord, item in grid.items():
        if item != PAPER:
            continue

        # A roll of paper is accessible if there are fewer than 4 adjacent rolls of paper.
        x, y = coord
        if (
            sum(
                1
                for n in [
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                    (x + 1, y + 1),
                    (x + 1, y - 1),
                    (x - 1, y + 1),
                    (x - 1, y - 1),
                ]
                if grid.get(n) == PAPER
            )
            < 4
        ):
            count_accessible_paper_rolls += 1

    return count_accessible_paper_rolls


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)
    known_paper_coords = {coord for coord, item in grid.items() if item == PAPER}

    total_removed = 0
    while True:
        to_remove = set()

        # A roll of paper is accessible if there are fewer than 4 adjacent rolls of paper.
        for x, y in known_paper_coords:
            if (
                sum(
                    1
                    for n in [
                        (x + 1, y),
                        (x - 1, y),
                        (x, y + 1),
                        (x, y - 1),
                        (x + 1, y + 1),
                        (x + 1, y - 1),
                        (x - 1, y + 1),
                        (x - 1, y - 1),
                    ]
                    if grid.get(n) == "@"
                )
                < 4
            ):
                to_remove.add((x, y))

        if to_remove:
            # Remove all the rolls of paper that are accessible in this pass.
            total_removed += len(to_remove)
            for loc in to_remove:
                grid[loc] = "."
                known_paper_coords.remove(loc)
        else:
            # No more rolls can be removed, we can stop now.
            break

    return total_removed


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

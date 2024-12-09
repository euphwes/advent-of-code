from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 10
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _neighbors(coord, trails):

    height = trails[coord]
    neighbors = list()

    cx, cy = coord
    for neighbor_coord in [(cx, cy + 1), (cx, cy - 1), (cx + 1, cy), (cx - 1, cy)]:
        if neighbor_coord not in trails:
            continue

        if trails[neighbor_coord] == height + 1:
            neighbors.append(neighbor_coord)

    return neighbors


def _walk_v0(coord, trails):
    neighbors = _neighbors(coord, trails)
    if any(trails[c] == 9 for c in neighbors):
        return sum(1 for c in neighbors if trails[c] == 9)

    return sum(_walk_v0(c, trails) for c in neighbors)


def _score_v0(trailhead, trails):
    score = _walk_v0(trailhead, trails)
    # print(f"{trailhead=} has {score=}")
    return score


def _walk_v1(coord, trails):
    neighbors = _neighbors(coord, trails)

    peaks = set()
    for neighbor in neighbors:
        if trails[neighbor] == 9:
            peaks.add(neighbor)
        else:
            peaks.update(_walk_v1(neighbor, trails))

    return peaks


def _score_v1(trailhead, trails):
    peaks = _walk_v1(trailhead, trails)
    # print(f"{trailhead=} has score={len(peaks)}")
    return len(peaks)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    trails = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            try:
                trails[(x, y)] = int(char)
            except ValueError:
                trails[(x, y)] = "."

    trailheads = set()
    for coord, char in trails.items():
        if char == 0:
            trailheads.add(coord)

    score = 0
    for trailhead in trailheads:
        score += _score_v1(trailhead, trails)

    return score


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    trails = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            try:
                trails[(x, y)] = int(char)
            except ValueError:
                trails[(x, y)] = "."

    trailheads = set()
    for coord, char in trails.items():
        if char == 0:
            trailheads.add(coord)

    score = 0
    for trailhead in trailheads:
        score += _score_v0(trailhead, trails)

    return score


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

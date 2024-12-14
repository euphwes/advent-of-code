from collections import defaultdict
from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 23
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _parse_network(raw_input: list[str]) -> dict[str, set[str]]:
    network = defaultdict(set)
    for line in raw_input:
        parts = line.split("-")
        network[parts[0]].add(parts[1])
        network[parts[1]].add(parts[0])

    return dict(network)


def _find_groups(network: dict[str, set[str]], group_size: int = 3) -> list[set[str]]:
    groups = set()
    for node, connections in network.items():
        for combo in combinations(connections, group_size - 1):
            is_valid_group = True
            for subcombo in combinations(combo, 2):
                sc1, sc2 = subcombo
                if sc1 not in network[sc2]:
                    is_valid_group = False
                    break
            if is_valid_group:
                groups.add(frozenset({node, *combo}))

    return [set(group) for group in groups]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    network = _parse_network(raw_input)
    groups = _find_groups(network, group_size=3)
    return sum(1 for group in groups if any(node[0] == "t" for node in group))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    network = _parse_network(raw_input)
    num_nodes = len(network)

    for size in range(num_nodes, 3, -1):
        groups = _find_groups(network, group_size=size)
        if groups:
            assert len(groups) == 1
            return ",".join(sorted(groups[0]))

    return None


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

from dataclasses import dataclass
from itertools import combinations
from math import prod
from typing import Self

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 8
YEAR = 2025

PART_ONE_DESCRIPTION = "product of size of 3 largest circuits after 1000 connections made"
PART_ONE_ANSWER = 80446

PART_TWO_DESCRIPTION = "product of X coords of last 2 boxes connected to form 1 giant circuit"
PART_TWO_ANSWER = 51294528


Coord = tuple[int, int, int]


@dataclass(eq=True)
class Node:
    coord: Coord
    connected: set[Self]

    def __hash__(self) -> int:
        return hash(self.coord)

    def is_in_circuit(
        self,
        other: Self,
        already_checked: set[Self] | None = None,
    ) -> bool:
        """Return if the other Node is in the same circuit as this Node."""

        if other.coord == self.coord:
            return True

        if other in self.connected:
            return True

        already = set(already_checked) | {self} if already_checked else {self}
        # already.add(self)

        return any(
            child.is_in_circuit(other, already_checked=already)
            for child in self.connected
            if child not in already
        )


def _parse(raw_input: list[str]) -> list[Node]:
    """Parse 3D coordinates from the input file."""

    coords: list[Coord] = []

    for line in raw_input:
        x, y, z = tuple(line.split(","))
        coords.append((int(x), int(y), int(z)))

    return [Node(coord=coord, connected=set()) for coord in coords]


def _distance(n1: Node, n2: Node) -> int:
    """Calculate Euclidean distance between a pair of 3D coordinates."""

    x1, y1, z1 = n1.coord
    x2, y2, z2 = n2.coord

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    nodes = _parse(raw_input)

    # For every pair of nodes, store a tuple of distance between them, and the two nodes,
    # sorted from smallest to greatest distance.
    distance_of_node_pairs = sorted(
        [(_distance(node1, node2), node1, node2) for node1, node2 in combinations(nodes, 2)],
        key=lambda t: t[0],
    )

    # For the first 1000 pairs (sorted by their distance), connect the two nodes if they are
    # not already part of the same circuit.
    for _, node1, node2 in distance_of_node_pairs[:1000]:
        if node1.is_in_circuit(node2):
            continue
        node1.connected.add(node2)
        node2.connected.add(node1)

    # Hold groups of nodes that are connected to one another.
    circuits: list[set[Node]] = []

    # Loops over nodes, adding them to a "circuit" (group of connected nodes).
    for node in nodes:
        added = False
        for circuit in circuits:
            # Add to an existing circuit this node is connected to, if one exists.
            if any(other.is_in_circuit(node) for other in circuit):
                circuit.add(node)
                added = True
                break
        if not added:
            # Otherwise, start a new circuit with this node.
            circuits.append({node})

    # Create a list of circuit sizes, from largest to smallest.
    circuit_sizes = sorted([len(circuit) for circuit in circuits], reverse=True)

    return prod(circuit_sizes[:3])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    nodes = _parse(raw_input)

    # For every pair of nodes, store a tuple of distance between them, and the two nodes,
    # sorted from smallest to greatest distance.
    distance_of_node_pairs = sorted(
        [(_distance(node1, node2), node1, node2) for node1, node2 in combinations(nodes, 2)],
        key=lambda t: t[0],
    )

    # Continuously make connections between pairs of nodes, 1 at a time.
    while True:
        _, node1, node2 = distance_of_node_pairs.pop(0)
        if node1.is_in_circuit(node2):
            continue

        node1.connected.add(node2)
        node2.connected.add(node1)

        # Are all nodes connected as part of the same circuit?
        # If so, return the product of the X coordinates of the node pair just connected.
        test_node = nodes[0]
        if all(test_node.is_in_circuit(other_node) for other_node in nodes):
            return node1.coord[0] * node2.coord[0]


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

from collections import defaultdict
from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 25
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def pairwise(iterable):
    a, b = iter(iterable), iter(iterable)
    next(b, None)
    return zip(a, b)


def _bfs(start_node, target_node, node_edges_map):
    q = [(start_node, [start_node])]
    visited = set()

    while q:
        node, pathway = q.pop(0)
        visited.add(node)

        if node == target_node:
            return pathway

        for tnode in node_edges_map[node]:
            if tnode in visited:
                continue
            new_path = pathway + [tnode]
            q.append((tnode, new_path))

    return None


def _get_all_reachable_nodes(start_node, node_edges_map, edges_to_omit):
    reachable_nodes = set()
    q = [start_node]

    while q:
        node = q.pop()
        reachable_nodes.add(node)

        for tnode in node_edges_map[node]:
            if frozenset([tnode, node]) in edges_to_omit:
                continue
            if tnode in reachable_nodes:
                continue
            reachable_nodes.add(tnode)
            q.append(tnode)

    return reachable_nodes


def _partitions_without_edges(edges_to_omit, node_edges_map):
    partitions = set()
    q = list(node_edges_map.keys())

    while q:
        node = q.pop()

        if any(node in partition for partition in partitions):
            continue

        reachable_nodes = _get_all_reachable_nodes(node, node_edges_map, edges_to_omit)
        partitions.add(frozenset(reachable_nodes))

    return partitions


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    # 3462 edges
    # 1551 nodes

    node_edges_map = defaultdict(set)
    raw_edges = set()

    for line in stuff:
        node, target_nodes = line.split(": ")
        target_nodes = target_nodes.split()
        for target_node in target_nodes:
            node_edges_map[node].add(target_node)
            node_edges_map[target_node].add(node)
            raw_edges.add(frozenset([node, target_node]))

    print("counting edge traversals in all pairwise minimum node paths")
    count = 0
    edge_traversal_counts = defaultdict(int)
    for n1, n2 in combinations(node_edges_map.keys(), 2):
        count += 1
        if count % 1_000 == 0:
            print(f"{count:_} out of 1_202_025 for C(1551, 2)")
        pathway = _bfs(n1, n2, node_edges_map)

        # TODO: does a --> b --> c --> d found for (a, d)
        # imply that a --> b --> c is the shortest from a to c?
        # and that b --> c --> d is the shortest from b to d? It must...
        # so we can count those the appropriate number of times and record that we've already
        # found the shortest path for those pairs of nodes, too
        for e1, e2 in pairwise(pathway):
            edge_traversal_counts[frozenset([e1, e2])] += 1

    edge_and_counts = [(edge, count) for edge, count in edge_traversal_counts.items()]
    # sort by count high to low
    edge_and_counts.sort(key=lambda x: x[1], reverse=True)
    most_frequent_edges = [edge for edge, count in edge_and_counts[:100]]

    attempts = 0
    for e1, e2, e3 in combinations(most_frequent_edges, 3):
        attempts += 1
        if attempts % 1_000 == 0:
            print(f"{attempts:_} out of 167_100 for C(100, 3)")
        partitions = list(_partitions_without_edges(set([e1, e2, e3]), node_edges_map))
        if len(partitions) == 2:
            return len(partitions[0]) * len(partitions[1])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    pass


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

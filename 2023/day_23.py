from collections import defaultdict
from util.decorators import aoc_output_formatter
from util.input import get_input

from math import inf

DAY = 23
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


NEGATIVE_INFINITY = inf * -1


def _find_junctions(maze):
    junctions = set()

    sx = 0
    while True:
        if maze[(sx, 0)] == ".":
            # print(f"found start at {(sx, 0)}, calling it a junction")
            junctions.add((sx, 0))
            break
        else:
            sx += 1

    ex = 0
    maxy = max(y for _, y in maze.keys())
    while True:
        if maze[(ex, maxy)] == ".":
            # print(f"found end at {(ex, maxy)}, calling it a junction")
            junctions.add((ex, maxy))
            break
        else:
            ex += 1

    for coord, char in maze.items():
        if char != ".":
            continue

        cx, cy = coord
        neighs = list()
        for dx, dy in (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ):
            nx, ny = cx + dx, cy + dy
            if (nx, ny) in maze and maze[(nx, ny)] in ".<>^v":
                neighs.append((nx, ny))
        if len(neighs) > 2:
            neighs_repr = "".join([maze[n] for n in neighs])
            # print(f"{coord} is a junction with these neighbors: {neighs_repr}")
            junctions.add(coord)

    return junctions


def _get_start_end(maze):
    start = None
    end = None

    sx = 0
    while True:
        if maze[(sx, 0)] == ".":
            # print(f"found start at {(sx, 0)}, calling it a junction")
            start = (sx, 0)
            break
        else:
            sx += 1

    ex = 0
    maxy = max(y for _, y in maze.keys())
    while True:
        if maze[(ex, maxy)] == ".":
            # print(f"found end at {(ex, maxy)}, calling it a junction")
            end = (ex, maxy)
            break
        else:
            ex += 1

    return start, end


def _walk_junctions_get_edge_weights(maze):
    junctions = _find_junctions(maze)
    edge_weights = defaultdict(list)

    for junction in junctions:
        # print(f"\nWalking {junction}")
        jx, jy = junction
        for dx, dy in (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ):
            nx, ny = jx + dx, jy + dy
            if (nx, ny) in maze and maze[(nx, ny)] in ".^<>v":
                # if dx == -1 and maze[(nx, ny)] == ">":
                #     continue
                # if dx == 1 and maze[(nx, ny)] == "<":
                #     continue
                # if dy == -1 and maze[(nx, ny)] == "v":
                #     continue
                # if dy == 1 and maze[(nx, ny)] == "^":
                #     continue

                visited = set()
                visited.add((jx, jy))
                visited.add((nx, ny))
                steps = 1

                while True:
                    found_jn = False
                    neighs = list()
                    for dx, dy in (
                        (1, 0),
                        (-1, 0),
                        (0, 1),
                        (0, -1),
                    ):
                        nnx, nny = nx + dx, ny + dy
                        # print(f"looking at {(nnx, nny)}")
                        if (nnx, nny) not in visited and maze[(nnx, nny)] in ".<>^v":
                            if (nnx, nny) in junctions:
                                # print(
                                #     f"{steps+1} steps between {(jx, jy)} and {(nnx, nny)}"
                                # )
                                edge_weights[(jx, jy)].append(((nnx, nny), steps + 1))
                                found_jn = True
                                break
                            else:
                                neighs.append((nnx, nny))

                    if found_jn:
                        break

                    if len(neighs) == 1:
                        nx, ny = neighs[0]
                        visited.add((nx, ny))
                        steps += 1

    return edge_weights


def _get_path_lengths(jn, edge_weights, target, visited):
    # print(f"at {jn} having already visited {visited}")
    path_lengths = []

    for next_jn, weight in edge_weights[jn]:
        if next_jn == target:
            path_lengths.append(weight)
            continue

        if next_jn in visited:
            continue

        v_copy = {x for x in visited}
        v_copy.add(next_jn)
        for remaining_path_len in _get_path_lengths(
            next_jn, edge_weights, target, v_copy
        ):
            path_lengths.append(weight + remaining_path_len)

    return [] if not path_lengths else [max(path_lengths)]
    return [max(path_lengths)]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    maze = defaultdict(lambda: "#")
    for y, row in enumerate(stuff):
        for x, char in enumerate(row):
            maze[x, y] = char

    start, end = _get_start_end(maze)
    edge_weights = _walk_junctions_get_edge_weights(maze)
    from pprint import pprint

    # print(start)
    # print(end)
    # pprint(edge_weights)

    path_lengths = _get_path_lengths(start, edge_weights, end, set())
    # print(path_lengths)
    return max(path_lengths)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    pass


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

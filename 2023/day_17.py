from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heapify, heappop, heappush

# from itertools import pairwise
from math import inf as INFINITY
from random import choice
from typing import Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 17
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def pairwise(myiter):
    for x in range(len(myiter) - 1):
        yield myiter[x], myiter[x + 1]


@dataclass
class SearchState:
    x: int
    y: int
    history: Tuple[str, str, str]
    heat_loss: int

    @property
    def coord(self):
        return self.x, self.y

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss


OPPOSITE_DIRECTION_MAP = {
    "r": "l",
    "l": "r",
    "u": "d",
    "d": "u",
}

DP = dict()


def _get_neighbors(curr_state, hl_map):
    x, y = curr_state.x, curr_state.y

    key = (*curr_state.coord, *curr_state.history)
    if key in DP:
        return DP[key]

    neighbors = []

    for potential_neighbor in (
        (x + 1, y, "r"),
        (x - 1, y, "l"),
        (x, y + 1, "d"),
        (x, y - 1, "u"),
    ):
        (nx, ny), direction = potential_neighbor[:2], potential_neighbor[2]

        # Can't go off the map
        if (nx, ny) not in hl_map:
            continue

        # Can't take more than 3 steps in the same direction
        if all(step == direction for step in curr_state.history):
            continue

        # Can't go back the previous direction
        if curr_state.history[-1] == OPPOSITE_DIRECTION_MAP[direction]:
            continue

        neighbors.append(
            SearchState(
                nx,
                ny,
                (*curr_state.history[1:], direction),
                curr_state.heat_loss + hl_map[(nx, ny)],
            )
        )

    DP[key] = neighbors
    return neighbors


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    target = -1, -1
    hl_map = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            hl_map[(x, y)] = int(char)
            target = (x, y)

    visited = set()
    q = []
    # heappush(q, SearchState(0, 0, ("x", "x", "x"), 0))
    q.append(SearchState(0, 0, ("x", "x", "x"), 0))

    result_map = defaultdict(lambda: INFINITY)

    while q:
        # curr_state = heappop(q)
        curr_state = q.pop(0)
        # print(curr_state)
        visited.add(curr_state.coord)

        q = [s for s in q if s.coord not in visited]
        # heapify(q)

        for next_state in _get_neighbors(curr_state, hl_map):
            if next_state.coord not in visited:
                result_map[next_state.coord] = min(
                    result_map[next_state.coord], next_state.heat_loss
                )
                # heappush(q, next_state)
                q.append(next_state)

    return result_map[target]


def _is_valid_history(history):
    for p1, p2 in pairwise(history):
        if p2 != " " and p1 == OPPOSITE_DIRECTION_MAP[p2]:
            return False
        if p2 == " " and p1 != " ":
            return False

    return True


def _physical_neighbors_and_dir(coord):
    x, y = coord
    return [
        ((x + 1, y), "r"),
        ((x - 1, y), "l"),
        ((x, y + 1), "d"),
        ((x, y - 1), "u"),
    ]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    target = -1, -1
    hl_map = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            if x >= 60 and x <= 80 and y >= 60 and y <= 80:
                continue
            hl_map[(x, y)] = int(char)
            target = (x, y)

    # for y in range(0, 142):
    #     line = ""
    #     for x in range(0, 142):
    #         line += str(hl_map.get((x, y), " "))
    #     print(line)

    # -------------------

    # key = ((x, y), direction, howlong)
    edge_weights = defaultdict(list)

    for root_coord in hl_map.keys():
        for run_length in range(1, 11):
            for direction in "ruld":
                key = (root_coord, direction, run_length)
                for neigh, ndir in _physical_neighbors_and_dir(root_coord):
                    if neigh not in hl_map:
                        continue
                    if ndir == OPPOSITE_DIRECTION_MAP[direction]:
                        continue
                    if run_length < 4 and ndir != direction:
                        continue
                    if run_length == 10 and ndir == direction:
                        continue
                    weight = hl_map[neigh]

                    if ndir == direction:
                        neigh_key = (neigh, direction, run_length + 1)
                    else:
                        neigh_key = (neigh, ndir, 1)
                    edge_weights[key].append((neigh_key, weight))

    # -------------------

    edge_weights[((0, 0), "r", 0)] = [
        (((1, 0), "r", 1), hl_map[(1, 0)]),
        (((0, 1), "d", 1), hl_map[(0, 1)]),
    ]

    # sample
    # edge_weights[((0, 0), "r", 0)] = [(((1, 0), "r", 1), 4), (((0, 1), "d", 1), 3)]

    visited = set()
    q = []
    # heappush(q, SearchState(0, 0, ("x", "x", "x"), 0))

    # weight, ((x, y), direction, howlong)
    heappush(q, (0, ((0, 0), "r", 0)))

    result_map = defaultdict(lambda: INFINITY)

    while q:
        curr_weight, state_info = heappop(q)

        curr_coord, curr_dir, curr_runlength = state_info
        # curr_history = tuple(coord_and_history[2:])

        # visited.add(curr_coord)
        visited.add(state_info)
        # print(f"{curr_coord=}")

        # if iters % 1200000 == 0:
        #     # if iters % 2500000 == 0:
        #     print("trimming")
        #     # trim the last 1/4 off the queue
        #     q = q[: 3 * (len(q) // 4)]

        #     # q = [s for s in q if s.coord not in visited]
        q = [s for s in q if tuple(s[1]) not in visited]
        # q = [s for s in q if tuple(s[1][0]) not in visited]
        heapify(q)

        for next_state, weight in edge_weights[state_info]:
            next_coord, next_dir, next_runlength = next_state
            # next_history = tuple(next_state[2:])
            if next_state not in visited:
                # if next_coord not in visited:
                # result_map[next_state] = min(
                #     result_map[next_state], weight + curr_weight
                # )
                if next_coord == target:
                    if next_runlength >= 4:
                        result_map[next_state] = min(
                            result_map[next_state], weight + curr_weight
                        )
                else:
                    # result_map[next_coord] = min(
                    #     result_map[next_coord], weight + curr_weight
                    # )
                    result_map[next_state] = min(
                        result_map[next_state], weight + curr_weight
                    )
                heappush(q, (weight + curr_weight, next_state))

    return min(v for k, v in result_map.items() if k[0] == target)
    return result_map[target]


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    # not 784, too high
    # not 769, too high
    # 759 ? (old soln with heuristic to trim last X% of queue)
    # 758 ? (old soln with heuristic to trim last X% of queue)
    # 768 ? (new soln, not sure if correct, trimmed the inside the square maybe too far)
    # part_one(stuff)

    stuff = get_input(input_file)

    # 895? I think that's wrong
    # 892? still prob too
    part_two(stuff)

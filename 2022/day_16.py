from collections import defaultdict
from copy import copy
from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 16
YEAR = 2022

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

VALVE_OPEN = "open"
VALVE_CLOSED = "closed"


def _parse_stuff(stuff):
    valve_state = defaultdict(lambda: VALVE_CLOSED)
    valve_flow_rate = defaultdict(int)
    valve_connections = defaultdict(set)

    for line in stuff:
        valve_info, dest_info = line.split("; ")
        valve_num = valve_info[6:8]
        valve_rate = int(valve_info[valve_info.index("=") + 1 :])

        dest_info = dest_info.replace("tunnels lead to valves ", "")
        dest_info = dest_info.replace("tunnel leads to valve ", "")
        valve_connections[valve_num] = dest_info.split(", ")

        valve_flow_rate[valve_num] = valve_rate
        valve_state[valve_num] = VALVE_CLOSED

    # All of the zero-valued flow rate valves, just consider them open to start with, because it
    # we don't need to consider them to be opened anyway.
    for valve, rate in valve_flow_rate.items():
        if rate == 0:
            valve_state[valve] = VALVE_OPEN

    return valve_state, valve_flow_rate, valve_connections


def _get_distance_between(a, b, connections):

    steps = 0
    queue = [(a, 0)]
    visited = set()

    while queue:
        curr, steps = queue.pop(0)
        if curr == b:
            return steps

        for neighbor in connections[curr]:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            queue.append((neighbor, steps + 1))  # type: ignore


#
def _get_distance_map(connections, valves_to_visit, starting_valve):

    distance_map = dict()

    relevant_valves = copy(valves_to_visit)
    relevant_valves.add(starting_valve)

    for a, b in combinations(relevant_valves, 2):

        distance = _get_distance_between(a, b, connections)
        distance_map[(a, b)] = distance
        distance_map[(b, a)] = distance


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    valve_distances = _get_distance_map(connections, valves_to_visit, "AA")


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    starting_states, rates, conns = _parse_stuff(stuff)
    minutes = 26


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)
    part_one(stuff)

    # stuff = get_input(input_file)
    # part_two(stuff)

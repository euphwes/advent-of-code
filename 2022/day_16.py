from collections import defaultdict

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

        valve_flow_rate[valve_num] = valve_rate

        dest_info = dest_info.replace("tunnels lead to valves ", "")
        dest_info = dest_info.replace("tunnel leads to valve ", "")
        valve_connections[valve_num] = dest_info.split(", ")

        valve_state[valve_num] = VALVE_CLOSED

    return valve_state, valve_flow_rate, valve_connections


def _yield_all_walks_of_len(n, curr_valve, conns):

    walks_from_curr = list()
    for neighbor in conns[curr_valve]:
        walks_from_curr.append([neighbor])

    if n == 1:
        yield from walks_from_curr
    else:
        for walk in walks_from_curr:
            next_valve = walk[0]
            for shorter_walk in _yield_all_walks_of_len(n - 1, next_valve, conns):
                yield walk + shorter_walk


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    starting_states, rates, conns = _parse_stuff(stuff)
    minutes = 3

    curr_valve = "AA"
    prev_valve = None

    for walk in _yield_all_walks_of_len(minutes, curr_valve, conns):
        print(walk)

    return f"visited all walks of len={minutes}"


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

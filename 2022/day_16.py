from collections import defaultdict
from copy import copy
from itertools import combinations
from re import I

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

    raise ValueError(f"Couldn't find path between {a} and {b},")


def _get_distance_map(connections, valves_to_visit, starting_valve):

    distance_map = dict()

    relevant_valves = copy(valves_to_visit)
    relevant_valves.add(starting_valve)

    for a, b in combinations(relevant_valves, 2):

        # It takes 1 minute to open the valve when you arrive, let's just account for that here
        distance = _get_distance_between(a, b, connections) + 1
        distance_map[(a, b)] = distance
        distance_map[(b, a)] = distance

    return distance_map


def _scores_possible(
    curr_valve,
    valves_to_visit,
    rates,
    distances,
    minutes_left,
    score,
    valves_visited,
):

    if minutes_left <= 0:
        return [(0, valves_to_visit, valves_visited)]

    if not valves_to_visit:
        return [(0, set(), valves_visited)]

    valve_and_scores_and_remaining_valves_and_remaining_time_and_visited = list()

    for next_valve in valves_to_visit:
        # print()
        # print(f"check curr={curr_valve}, next={next_valve}")
        distance = distances[(curr_valve, next_valve)]
        if distance > minutes_left:
            continue

        this_next_valve_min_left = minutes_left - distance
        this_next_valve_score = this_next_valve_min_left * rates[next_valve]

        visited_so_far = copy(valves_visited) + [
            (next_valve, f"min={this_next_valve_min_left}")
        ]

        # print()
        # print(f"b={valves_to_visit}")
        next_remaining_valves = {v for v in valves_to_visit if v != next_valve}
        # print(f"a={next_remaining_valves}")

        valve_and_scores_and_remaining_valves_and_remaining_time_and_visited.append(
            (
                next_valve,
                this_next_valve_score,
                next_remaining_valves,
                this_next_valve_min_left,
                visited_so_far,
            )
        )

    next_scores_and_remaining_and_visited = list()

    for (
        next_valve,
        next_starting_score,
        next_remaining_valves,
        next_min_left,
        visited_so_far,
    ) in valve_and_scores_and_remaining_valves_and_remaining_time_and_visited:
        for total_next_score, remaining, visited_so_far in _scores_possible(
            next_valve,
            next_remaining_valves,
            rates,
            distances,
            next_min_left,
            next_starting_score,
            visited_so_far,
        ):
            next_scores_and_remaining_and_visited.append(
                (score + total_next_score, remaining, visited_so_far)
            )

    return next_scores_and_remaining_and_visited


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    start_valve = "AA"
    total_minutes = 30

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    scores_and_remaining_and_visited = _scores_possible(
        start_valve,
        valves_to_visit,
        valve_rates,
        valve_distances,
        total_minutes,
        0,
        list(),
    )
    scores_and_remaining_and_visited.sort(key=lambda x: x[0])

    score, remaining, visited = scores_and_remaining_and_visited[-1]
    print()
    print(f"{score=}")
    print(f"{remaining=}")
    print(f"{visited=}")
    print()
    return scores_and_remaining_and_visited[-1][0]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    # TODO for every result in _scores_possible for the elf with minutes = 26, run the elephant
    # for 26 minutes with the remaining valves.
    # IMPORTANT you can remove some elements of the results of _scores_possible, you only need
    # to consider the max score for each unique set of valves visited

    start_valve = "AA"
    total_minutes = 26

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    elf_scores_and_remaining = _scores_possible(
        start_valve,
        valves_to_visit,
        valve_rates,
        valve_distances,
        total_minutes,
        0,
        list(),
    )

    total_scores = list()

    best_scores_for_remaining = defaultdict(int)
    for elf_score, remaining_to_visit, _ in elf_scores_and_remaining:
        if elf_score > best_scores_for_remaining[frozenset(remaining_to_visit)]:
            best_scores_for_remaining[frozenset(remaining_to_visit)] = elf_score

    for remaining_to_visit, elf_score in best_scores_for_remaining.items():
        elephant_scores_and_remaining = _scores_possible(
            start_valve,
            remaining_to_visit,
            valve_rates,
            valve_distances,
            total_minutes,
            0,
            list(),
        )
        elephant_scores_and_remaining.sort(key=lambda x: x[0])
        best_elephant_score = elephant_scores_and_remaining[-1][0]
        total_scores.append(elf_score + best_elephant_score)

    # not 2206 (in 66 seconds, or again in 20 seconds, with improvement)
    return max(total_scores)


@aoc_output_formatter(YEAR, DAY, 3, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_three(stuff):

    start_valve = "AA"
    total_minutes = 26

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    little_under_half = (len(valves_to_visit) // 2) - 3
    little_over_half = (len(valves_to_visit) // 2) + 3

    best_score = 0

    for elf_set_size in range(1, len(valve_distances)):
        for elf_valves_combo in combinations(valves_to_visit, elf_set_size):
            elf_valves = set(elf_valves_combo)
            elephant_valves = set(valves_to_visit) - elf_valves
            # print()
            # print(elf_valves)
            # print(elephant_valves)

            elephant_scores_and_remaining = _scores_possible(
                start_valve,
                elephant_valves,
                valve_rates,
                valve_distances,
                total_minutes,
                0,
                list(),
            )
            if not elephant_scores_and_remaining:
                best_elephant_score = 0
            else:
                elephant_scores_and_remaining.sort(key=lambda x: x[0])
                best_elephant_score = elephant_scores_and_remaining[-1][0]

            elf_scores_and_remaining = _scores_possible(
                start_valve,
                elf_valves,
                valve_rates,
                valve_distances,
                total_minutes,
                0,
                list(),
            )
            if not elf_scores_and_remaining:
                best_elf_score = 0
            else:
                elf_scores_and_remaining.sort(key=lambda x: x[0])
                best_elf_score = elf_scores_and_remaining[-1][0]

            best_score = max([best_score, best_elf_score + best_elephant_score])

    # not 2257
    return best_score


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)
    part_one(stuff)

    # stuff = get_input(input_file)
    # part_two(stuff)

    # stuff = get_input(input_file)
    # part_three(stuff)

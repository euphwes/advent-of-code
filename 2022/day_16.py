from collections import defaultdict
from copy import copy
from itertools import combinations
from re import I

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 16
YEAR = 2022

PART_ONE_DESCRIPTION = "Most pressure that a single elf can release alone in 30 minutes"
# PART_ONE_ANSWER = 1673  # my input
# PART_ONE_ANSWER = 1651  # sample input
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

    # All of the zero-valued flow rate valves, just consider them open to start with, because we
    # don't need to consider them to be opened anyway.
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

    # for pair, distance in distance_map.items():
    #     a, b = pair
    #     if b < a:
    #         continue
    #     print(f"{pair}: {distance}")

    # print()
    # print(f'AF: {distance_map[("AA", "FA")]}')
    # print(f'FG: {distance_map[("FA", "GA")]}')
    # print(f'GH: {distance_map[("GA", "HA")]}')
    # print(f'HI: {distance_map[("HA", "IA")]}')
    # print(f'IJ: {distance_map[("IA", "JA")]}')
    # print(f'JK: {distance_map[("KA", "JA")]}')
    # print(f'KL: {distance_map[("KA", "LA")]}')
    # print(f'LM: {distance_map[("MA", "LA")]}')
    # print(f'MN: {distance_map[("MA", "NA")]}')
    # print(f'NO: {distance_map[("OA", "NA")]}')
    # print(f'OP: {distance_map[("OA", "PA")]}')

    return distance_map


def _possible_paths(
    curr_valve,
    valves_to_visit,
    distances,
    minutes_left,
    valves_visited,
):
    if not valves_to_visit:
        return [(set(), valves_visited)]

    if minutes_left <= 0:
        return [(valves_to_visit, valves_visited)]

    valve_and_remaining_valves_and_remaining_time_and_visited = list()

    for next_valve in valves_to_visit:
        # print()
        # print(f"check curr={curr_valve}, next={next_valve}")
        distance = distances[(curr_valve, next_valve)]
        if distance > minutes_left:
            continue

        this_next_valve_min_left = minutes_left - distance

        # TODO check this assumption
        # if this_next_valve_min_left == 0:
        #     continue

        visited_so_far = copy(valves_visited) + [(next_valve, this_next_valve_min_left)]

        # print()
        # print(f"b={valves_to_visit}")
        next_remaining_valves = {v for v in valves_to_visit if v != next_valve}
        # print(f"a={next_remaining_valves}")

        valve_and_remaining_valves_and_remaining_time_and_visited.append(
            (
                next_valve,
                next_remaining_valves,
                this_next_valve_min_left,
                visited_so_far,
            )
        )

    if not valve_and_remaining_valves_and_remaining_time_and_visited:
        return [(set(), valves_visited)]

    # print(valve_and_remaining_valves_and_remaining_time_and_visited)
    # for (
    #     next_valve,
    #     next_remaining_valves,
    #     min_left,
    #     visited_so_far,
    # ) in valve_and_remaining_valves_and_remaining_time_and_visited:
    #     print()
    #     print(f"Next={next_valve}")
    #     print(f"Remaining={next_remaining_valves}")
    #     print(f"Min left={min_left}")
    #     print(f"Visted so far={visited_so_far}")
    # return

    next_scores_and_remaining_and_visited = list()

    for (
        next_valve,
        next_remaining_valves,
        next_min_left,
        visited_so_far,
    ) in valve_and_remaining_valves_and_remaining_time_and_visited:
        for remaining, visited_so_far in _possible_paths(
            next_valve,
            next_remaining_valves,
            distances,
            next_min_left,
            visited_so_far,
        ):
            next_scores_and_remaining_and_visited.append((remaining, visited_so_far))

    return next_scores_and_remaining_and_visited


def _score_path(path_info, rates):
    score = 0
    for valve, min_remaining in path_info:
        score += rates[valve] * min_remaining
    return score


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    start_valve = "AA"
    total_minutes = 30

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    print(valves_to_visit)
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    remaining_and_visited = _possible_paths(
        start_valve,
        valves_to_visit,
        valve_distances,
        total_minutes,
        list(),
    )

    best_score = 0
    best_visited = []
    for _, visited in remaining_and_visited:
        this_score = _score_path(visited, valve_rates)
        if this_score > best_score:
            best_score = this_score
            best_visited = visited

    print()
    print(best_visited)
    print()
    debug_score_so_far = 0
    releasing = list()
    for valve, min_left in best_visited:
        rate = valve_rates[valve]
        released = rate * min_left
        print(
            f"Visited {valve} with rate {rate} with {min_left} min left, releasing {released}."
        )
        releasing.append(released)
    print()
    print(f"Sum({releasing})={sum(releasing)}")
    return best_score


@aoc_output_formatter(
    YEAR, DAY, "2 v1", PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER
)
def part_two_v1(stuff):

    # Overall idea -- let the elf run for 26 minutes and try to visit ALL valves.
    # For each path that's available to him in 26 minutes, give the remaining valves to the
    # elephant and have the elephant run them all for 26 minutes. Find the best result for the
    # elephant with the remaining valves, and then find the best sum of elf + elephant.

    start_valve = "AA"
    total_minutes = 26

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    elf_remaining_and_visited = _possible_paths(
        start_valve,
        valves_to_visit,
        valve_distances,
        total_minutes,
        list(),
    )

    best_total_score = 0

    for elf_remaining, elf_visited in elf_remaining_and_visited:

        elf_score = _score_path(elf_visited, valve_rates)

        # print(elf_remaining)
        elephant_remaining_and_visited = _possible_paths(
            start_valve,
            elf_remaining,
            valve_distances,
            total_minutes,
            list(),
        )

        best_elephant_score = 0
        for _, elephant_visited in elephant_remaining_and_visited:
            best_elephant_score = max(
                [best_elephant_score, _score_path(elephant_visited, valve_rates)]
            )
            # if best_elephant_score == _score_path(elephant_visited, valve_rates):
            #     remember_elephant_visited = elephant_visited

        best_total_score = max([best_total_score, elf_score + best_elephant_score])
        # if best_total_score == best_elephant_score + elf_score:
        #     print()
        #     print("New best, happens with")
        #     print(f"Elf: {elf_visited}")
        #     print(f"Elephant: {remember_elephant_visited}")

    # not 2206 (in 66 seconds, or again in 20 seconds, with improvement)
    return best_total_score


@aoc_output_formatter(
    YEAR, DAY, "2 v2", PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER
)
def part_two_v2(stuff):

    # Overall idea -- for every possible number of valves, for all combinations within that
    # number, let the elf run and get his possible paths. For each possible path, give the
    # unvisited valves to the elephant and let him run. Find the best score.

    start_valve = "AA"
    total_minutes = 26

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    best_score = 0

    for elf_set_size in range(1, len(valves_to_visit)):
        for elf_valves_combo in combinations(valves_to_visit, elf_set_size):

            elf_valves = set(elf_valves_combo)

            elf_remaining_and_visited = _possible_paths(
                start_valve,
                elf_valves,
                valve_distances,
                total_minutes,
                list(),
            )

            for elf_remaining, elf_visited in elf_remaining_and_visited:
                elf_score = _score_path(elf_visited, valve_rates)

                elephant_remaining_and_visited = _possible_paths(
                    start_valve,
                    set(elf_remaining),
                    valve_distances,
                    total_minutes,
                    list(),
                )

                best_elephant_score = 0
                for _, elph_visited in elephant_remaining_and_visited:
                    best_elephant_score = max(
                        [best_elephant_score, _score_path(elph_visited, valve_rates)]
                    )

                best_score = max([best_score, elf_score + best_elephant_score])

    # not 2257, not 2297
    return best_score


@aoc_output_formatter(YEAR, DAY, 4, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_four(stuff):

    start_valve = "AA"
    total_minutes = 26

    valve_states, valve_rates, connections = _parse_stuff(stuff)

    # These are the only valves that we need to worry about visiting.
    valves_to_visit = {
        valve for valve, state in valve_states.items() if state == VALVE_CLOSED
    }
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    little_under_half = (len(valves_to_visit) // 2) - 2
    little_over_half = (len(valves_to_visit) // 2) + 2

    best_score = 0

    for elf_set_size in range(little_under_half, little_over_half + 1):
        # for elf_set_size in range(1, len(valves_to_visit)):
        for elf_valves_combo in combinations(valves_to_visit, elf_set_size):

            elf_valves = set(elf_valves_combo)
            elephant_valves = set(valves_to_visit) - elf_valves

            elf_remaining_and_visited = _possible_paths(
                start_valve,
                elf_valves,
                valve_distances,
                total_minutes,
                list(),
            )

            best_elf_score = 0
            for _, elf_visited in elf_remaining_and_visited:
                best_elf_score = max(
                    [best_elf_score, _score_path(elf_visited, valve_rates)]
                )

            elephant_remaining_and_visited = _possible_paths(
                start_valve,
                elephant_valves,
                valve_distances,
                total_minutes,
                list(),
            )

            best_elephant_score = 0
            for _, elph_visited in elephant_remaining_and_visited:
                best_elephant_score = max(
                    [best_elephant_score, _score_path(elph_visited, valve_rates)]
                )

            best_score = max([best_score, best_elf_score + best_elephant_score])

    # not 2257, not 2297
    return best_score


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)
    part_one(stuff)

    # stuff = get_input(input_file)
    # part_two_v1(stuff)

    # stuff = get_input(input_file)
    # part_three(stuff)

    stuff = get_input(input_file)
    part_four(stuff)

from collections import defaultdict
from copy import copy
from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 16
YEAR = 2022

PART_ONE_DESCRIPTION = "Most pressure that a single elf can release alone in 30 minutes"
PART_ONE_ANSWER = 1673

PART_TWO_DESCRIPTION = "Most pressure that elf + elephant duo can release in 26 minutes"
PART_TWO_ANSWER = 2343


def _parse_stuff(stuff):
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

    valves_to_visit = {v for v, r in valve_flow_rate.items() if r > 0}

    return valves_to_visit, valve_flow_rate, valve_connections


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


def _possible_paths(
    curr_valve,
    valves_to_visit,
    distances,
    minutes_left,
    valves_visited,
):
    if not valves_to_visit:
        return [valves_visited]

    if minutes_left <= 0:
        return [valves_visited]

    valve_and_remaining_valves_and_remaining_time_and_visited = list()

    for next_valve in valves_to_visit:
        distance = distances[(curr_valve, next_valve)]
        if distance > minutes_left:
            continue

        this_next_valve_min_left = minutes_left - distance

        visited_so_far = copy(valves_visited) + [(next_valve, this_next_valve_min_left)]

        next_remaining_valves = {v for v in valves_to_visit if v != next_valve}

        valve_and_remaining_valves_and_remaining_time_and_visited.append(
            (
                next_valve,
                next_remaining_valves,
                this_next_valve_min_left,
                visited_so_far,
            )
        )

    if not valve_and_remaining_valves_and_remaining_time_and_visited:
        return [valves_visited]

    next_scores_and_remaining_and_visited = list()

    for (
        next_valve,
        next_remaining_valves,
        next_min_left,
        visited_so_far,
    ) in valve_and_remaining_valves_and_remaining_time_and_visited:
        for visited_so_far in _possible_paths(
            next_valve,
            next_remaining_valves,
            distances,
            next_min_left,
            visited_so_far,
        ):
            next_scores_and_remaining_and_visited.append(visited_so_far)

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

    valves_to_visit, valve_rates, connections = _parse_stuff(stuff)
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    paths = _possible_paths(
        start_valve,
        valves_to_visit,
        valve_distances,
        total_minutes,
        list(),
    )

    return max(_score_path(path, valve_rates) for path in paths)


@aoc_output_formatter(YEAR, DAY, 4, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    start_valve = "AA"
    total_minutes = 26

    valves_to_visit, valve_rates, connections = _parse_stuff(stuff)
    valve_distances = _get_distance_map(connections, valves_to_visit, start_valve)

    little_under_half = (len(valves_to_visit) // 2) - 1
    little_over_half = (len(valves_to_visit) // 2) + 2

    best_score = 0

    for elf_set_size in range(little_under_half, little_over_half):
        for elf_valves_combo in combinations(valves_to_visit, elf_set_size):

            elf_valves = set(elf_valves_combo)
            elephant_valves = set(valves_to_visit) - elf_valves

            elf_paths = _possible_paths(
                start_valve,
                elf_valves,
                valve_distances,
                total_minutes,
                list(),
            )

            best_elf_score = 0
            for elf_path in elf_paths:
                best_elf_score = max(
                    [best_elf_score, _score_path(elf_path, valve_rates)]
                )

            elephant_paths = _possible_paths(
                start_valve,
                elephant_valves,
                valve_distances,
                total_minutes,
                list(),
            )

            best_elephant_score = 0
            for elephant_path in elephant_paths:
                best_elephant_score = max(
                    [best_elephant_score, _score_path(elephant_path, valve_rates)]
                )

            best_score = max([best_score, best_elf_score + best_elephant_score])

    return best_score


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

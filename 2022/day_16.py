from collections import defaultdict
from copy import copy

from util.decorators import aoc_output_formatter
from util.input import get_input

## TODO can we find cycles of 0-flow valves leading to one another and remove?
## how else to reduce search space?

DAY = 16
YEAR = 2022

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

VALVE_OPEN = "open"
VALVE_CLOSED = "closed"

DO_TRIM_MOST_PROMISING = False


def _trim_down(states_list, threshold_size, target_count):
    if not DO_TRIM_MOST_PROMISING:
        return states_list
    if len(states_list) > threshold_size:
        states_list.sort(key=lambda s: s.release_pressure)
        states_list = states_list[-1 * target_count :]
    return states_list


def _parse_stuff(stuff):
    valve_state = defaultdict(lambda: VALVE_CLOSED)
    valve_flow_rate = defaultdict(int)
    valve_connections = defaultdict(set)
    valves = set()

    for line in stuff:
        valve_info, dest_info = line.split("; ")
        valve_num = valve_info[6:8]
        valve_rate = int(valve_info[valve_info.index("=") + 1 :])

        valves.add(valve_num)
        valve_flow_rate[valve_num] = valve_rate

        dest_info = dest_info.replace("tunnels lead to valves ", "")
        dest_info = dest_info.replace("tunnel leads to valve ", "")
        valve_connections[valve_num] = dest_info.split(", ")

    return valve_state, valve_flow_rate, valve_connections, valves


class ValveVisitState:
    def __init__(
        self,
        elf_valve,
        elephant_valve,
        elf_previous,
        elephant_previous,
        states,
        release_pressure,
        min_remaining,
    ):
        self.elf_valve = elf_valve
        self.elephant_valve = elephant_valve
        self.elf_previous = elf_previous
        self.elephant_previous = elephant_previous
        self.states = states
        self.release_pressure = release_pressure
        self.minutes_remaining = min_remaining

    def elf_valve_is_closed(self):
        return self.states[self.elf_valve] == VALVE_CLOSED

    def elephant_valve_is_closed(self):
        return self.states[self.elephant_valve] == VALVE_CLOSED


def _get_states_at_depth(curr: ValveVisitState, rates, conns):

    next_elf_states = list()

    # ************ move elf first *************

    if curr.elf_valve_is_closed() and rates[curr.elf_valve] > 0:
        # we could open it
        next_states = copy(curr.states)
        next_states[curr.elf_valve] = VALVE_OPEN
        next_release_pressure = curr.release_pressure + (
            (curr.minutes_remaining - 1) * rates[curr.elf_valve]
        )
        next_elf_states.append(
            ValveVisitState(
                elf_valve=curr.elf_valve,
                elephant_valve=curr.elephant_valve,
                elf_previous=curr.elf_previous,
                elephant_previous=curr.elephant_previous,
                states=next_states,
                release_pressure=next_release_pressure,
                min_remaining=curr.minutes_remaining - 1,
            )
        )

    # or we could visit an adjacent valve, except it doesn't make sense to return backwards
    for neighbor in conns[curr.elf_valve]:
        if neighbor == curr.elf_previous and len(conns[curr.elf_valve]) > 1:
            continue
        next_elf_states.append(
            ValveVisitState(
                elf_valve=neighbor,
                elephant_valve=curr.elephant_valve,
                elf_previous=curr.elf_valve,
                elephant_previous=curr.elephant_previous,
                states=copy(curr.states),
                release_pressure=curr.release_pressure,
                min_remaining=curr.minutes_remaining - 1,
            )
        )

    # ************ move elephant next, modifying half-finished elf moved states *************

    # save memory, try to prune lowest flow states? maybe speed up
    # probably get rid of this in a good impl
    next_elf_states = _trim_down(next_elf_states, 2, 2)

    next_total_valve_states = list()

    for half_finished_state in next_elf_states:
        if (
            half_finished_state.elephant_valve_is_closed()
            and rates[half_finished_state.elephant_valve] > 0
        ):
            # elephant could open it
            elph_next_states = copy(half_finished_state.states)
            elph_next_states[half_finished_state.elephant_valve] = VALVE_OPEN
            elph_next_release_pressure = half_finished_state.release_pressure + (
                half_finished_state.minutes_remaining
                * rates[half_finished_state.elephant_valve]
            )

            # elf and elephant stay same place, next valve states and pressure changes
            # already updated minute above with elf
            next_total_valve_states.append(
                ValveVisitState(
                    elf_valve=half_finished_state.elf_valve,
                    elephant_valve=half_finished_state.elephant_valve,
                    elf_previous=half_finished_state.elf_previous,
                    elephant_previous=half_finished_state.elephant_previous,
                    states=elph_next_states,
                    release_pressure=elph_next_release_pressure,
                    min_remaining=half_finished_state.minutes_remaining,
                )
            )

        # or elephant could visit an adjacent valve, except it doesn't make sense to return backwards
        for neighbor in conns[half_finished_state.elephant_valve]:
            if (
                neighbor == half_finished_state.elephant_previous
                and len(conns[half_finished_state.elephant_valve]) > 1
            ):
                continue

            # doesn't make sense for the elephant to go where the elf was
            # this makes an empty list
            # if neighbor == half_finished_state.elf_previous:
            #     continue

            # update state rather than add new one
            # elf stays put, and elephant moves
            # minutes dont change
            next_total_valve_states.append(
                ValveVisitState(
                    elf_valve=half_finished_state.elf_valve,
                    elephant_valve=neighbor,
                    elf_previous=half_finished_state.elf_previous,
                    elephant_previous=half_finished_state.elephant_valve,
                    states=half_finished_state.states,
                    release_pressure=half_finished_state.release_pressure,
                    min_remaining=half_finished_state.minutes_remaining,
                )
            )

    # --------------- NOW both movements are done ------------------

    # if we're out of time, return these states
    if next_total_valve_states[0].minutes_remaining == 0:
        return next_total_valve_states

    # otherwise, we need to go a level deeper from each of these states
    # TODO we need to prune this because we're just going in circles

    # save memory, try to prune lowest flow states? maybe speed up
    # probably get rid of this in a good impl
    next_total_valve_states = _trim_down(next_total_valve_states, 4, 2)

    next_minute_states = list()
    for state in next_total_valve_states:
        next_minute_states.extend(_get_states_at_depth(state, rates, conns))

    # save memory, try to prune lowest flow states? maybe speed up
    # probably get rid of this in a good impl
    next_minute_states = _trim_down(next_minute_states, 4, 2)

    return next_minute_states


# @aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
# def part_one(stuff):

#     starting_states, rates, conns, valves = _parse_stuff(stuff)

#     visit_state = ValveVisitState(
#         valve="AA",
#         previous=None,
#         states=copy(starting_states),
#         release_pressure=0,
#         min_remaining=30,
#     )

#     all_states = _get_states_at_depth(visit_state, rates, conns)

#     # not 672
#     return max(s.release_pressure for s in all_states)


# ----------------------------------------------------------------------------------------------


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    starting_states, rates, conns, valves = _parse_stuff(stuff)

    minutes = 5

    visit_state = ValveVisitState(
        elf_valve="AA",
        elephant_valve="AA",
        elf_previous=None,
        elephant_previous=None,
        states=copy(starting_states),
        release_pressure=0,
        min_remaining=minutes,
    )

    all_states = _get_states_at_depth(visit_state, rates, conns)

    # not 1873
    foo = max(s.release_pressure for s in all_states)
    if foo != 102 and minutes == 5:
        print("Not right")
    return foo


# ----------------------------------------------------------------------------------------------


def run(input_file):

    # stuff = get_input(input_file)
    # part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

from collections import defaultdict
from copy import copy
from random import choice

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
    def __init__(self, valve, previous, states, release_pressure, min_remaining):
        self.valve = valve
        self.previous = previous
        self.states = states
        self.release_pressure = release_pressure
        self.minutes_remaining = min_remaining

    def curr_valve_is_closed(self):
        return self.states[self.valve] == VALVE_CLOSED


def _get_states_at_depth(curr: ValveVisitState, rates, conns):

    next_valve_states = list()

    # if curr.nothing_left_to_do():
    #     return [
    #         ValveVisitState(
    #             valve=curr.valve,
    #             states=curr.states,
    #             release_pressure=curr.release_pressure,
    #             min_remaining=0,
    #         )
    #     ]

    # if all non-zero valves are open, return same state but with time = 0 ?
    # if all(vs == VALVE_OPEN for v, vs in curr.states.items() if rates[v] > 0):
    #     return [
    #         ValveVisitState(
    #             valve=curr.valve,
    #             previous=curr.previous,
    #             states=curr.states,
    #             release_pressure=curr.release_pressure,
    #             min_remaining=curr.minutes_remaining - 1,
    #         )
    #     ]

    if curr.curr_valve_is_closed() and rates[curr.valve] > 0:
        # we could open it
        next_states = copy(curr.states)
        next_states[curr.valve] = VALVE_OPEN
        next_release_pressure = curr.release_pressure + (
            (curr.minutes_remaining - 1) * rates[curr.valve]
        )
        next_valve_states.append(
            ValveVisitState(
                valve=curr.valve,
                previous=curr.previous,
                states=next_states,
                release_pressure=next_release_pressure,
                min_remaining=curr.minutes_remaining - 1,
            )
        )

    # or we could visit an adjacent valve, except it doesn't make sense to return backwards
    for neighbor in conns[curr.valve]:

        if neighbor == curr.previous and len(conns[curr.valve]) > 1:
            continue
        next_valve_states.append(
            ValveVisitState(
                valve=neighbor,
                previous=curr.valve,
                states=copy(curr.states),
                release_pressure=curr.release_pressure,
                min_remaining=curr.minutes_remaining - 1,
            )
        )

    # if we're out of time, return these states
    if next_valve_states[0].minutes_remaining == 0:
        return next_valve_states

    # otherwise, we need to go a level deeper from each of these states
    # TODO we need to prune this because we're just going in circles

    # save memory, try to prune lowest flow states? maybe speed up
    next_valve_states.sort(key=lambda s: s.release_pressure)
    if len(next_valve_states) > 4:
        next_valve_states.sort(key=lambda s: s.release_pressure)
        next_valve_states = next_valve_states[-2:]
    # comment out above

    next_minute_states = list()
    for state in next_valve_states:
        next_minute_states.extend(_get_states_at_depth(state, rates, conns))

    # save memory, try to prune lowest flow states? maybe speed up
    if len(next_minute_states) > 4:
        next_minute_states.sort(key=lambda s: s.release_pressure)
        next_minute_states = next_minute_states[-2:]
        # for _ in range(1):
        #     next_minute_states.pop(0)
    # comment out above

    return next_minute_states


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    starting_states, rates, conns, valves = _parse_stuff(stuff)

    visit_state = ValveVisitState(
        valve="AA",
        previous=None,
        states=copy(starting_states),
        release_pressure=0,
        min_remaining=30,
    )

    all_states = _get_states_at_depth(visit_state, rates, conns)

    # not 672
    return max(s.release_pressure for s in all_states)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one_old(stuff):

    valve_state, valve_flow_rate, valve_connections, valves = _parse_stuff(stuff)

    pressure_released_options = list()

    for _ in range(999_000):
        minutes_remaining = 30
        pressure_release = 0
        current_valve = "AA"

        while minutes_remaining:
            if (
                valve_state[current_valve] == VALVE_CLOSED
                and valve_flow_rate[current_valve] > 0
            ):
                # valve is closed, but we don't necessarily need to open it now, it might
                # be better to spend a minute going to another
                if choice([0, 0, 0, 0, 1]) == 0:
                    # coin flip open now
                    # print(f"Opened {current_valve} at {minutes_remaining=}")
                    valve_state[current_valve] = VALVE_OPEN
                    minutes_remaining -= 1
                    pressure_release += (
                        minutes_remaining * valve_flow_rate[current_valve]
                    )
                    continue

            current_valve = choice(valve_connections[current_valve])
            minutes_remaining -= 1

        pressure_released_options.append(pressure_release)

    return max(pressure_released_options)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    pass


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)

    part_one(stuff)
    part_two(stuff)

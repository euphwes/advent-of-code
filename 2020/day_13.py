from util.decorators import aoc_output_formatter
from util.input import get_input

from functools import reduce
from math import gcd

#---------------------------------------------------------------------------------------------------

def __lcm(a, b):
    """ Returns the lowest common multiple of a and b. """

    return abs(a*b) // gcd(a, b)


def __simulate_buses(buses, start):
    """ Given a bus schedule as input (a list of bus IDs), this returns an endless generator which
    yields for every bus departure. This yields a tuple of the form (current_time, [bus IDs]). """

    t = start
    while True:
        buses_departing = [bus for bus in buses if t % bus == 0]
        if buses_departing:
            yield (t, buses_departing)
        t += 1

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 13, 1, 'first bus ID * time waited')
def part_one(earliest_time, buses):
    for t, buses in __simulate_buses(buses, earliest_time):
        return (t - earliest_time) * buses[0]


@aoc_output_formatter(2020, 13, 2, 'when buses depart in order, at the offsets in the schedule')
def part_two(offset_buses):

    # Grab the first bus ID. We'll start at time t = <first bus ID>, and also the time step will
    # start by being <first bus ID> as well. If the buses are departing in order, the timestamp
    # we're looking for must be a multiple of <first bus ID>
    first_bus = offset_buses[0][1]
    time_step = first_bus
    t = time_step

    check_departs = lambda t, bus: t % bus == 0

    # Separate the rest of the buses from the first, so we can check if those buses are departing
    # at the correct offset times relative to the first bus.
    rest_of_buses = offset_buses[1:]
    while True:
        # Start a list to hold all the bus IDs which are leaving at the correct offset relative
        # to the first bus.
        good_buses = [first_bus]

        # For each bus after the first, check if it's departing at (t + offset). If it is, that bus
        # is good, so add it to the list of good buses.
        for offset, bus in rest_of_buses:
            if check_departs(offset + t, bus):
                good_buses.append(bus)

        # If every bus is departing at the correct offset, this is the timestamp we're looking for!
        if len(good_buses) == len(offset_buses):
            return t

        # If some buses aren't departing at the right time, this isn't the correct timestamp.
        # Whichever subset of buses *are* departing at the correct time relative to each other allows
        # us to reduce the search space. To maintain the same relative spacing, the next timestamp
        # must be a multiple of all the bus IDs ahead of the current time. Find the LCM (lowest
        # common multiple) of all the bus IDs that are departing at the correct offsets, and that's
        # the new time step.
        time_step = reduce(__lcm, good_buses, 1)
        t += time_step

#---------------------------------------------------------------------------------------------------

def run(input_file):

    input_lines = get_input(input_file)
    earliest_time = int(input_lines[0])
    buses = [int(n) for n in input_lines[1].split(',') if n != 'x']

    part_one(earliest_time, buses)

    offset_buses = [(i, int(n)) for i, n in enumerate(input_lines[1].split(',')) if n != 'x']
    part_two(offset_buses)

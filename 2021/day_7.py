from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _determine_minimal_crab_fuel(crabs, fuel_cost_function):
    """ Given a population of crabs at various horizontal positions, and a function to determine
    how much fuel it costs to move a crab to a target position, return the minimal amount of fuel
    required to align the crabs at a single target horizontal position. """

    fuel_cost_options = list()

    # For each position the crabs can align to, calc how much total fuel is required to get there.
    for target_position in set(crabs):
        fuel = 0
        for crab_position in crabs:
            fuel += fuel_cost_function(crab_position, target_position)
        fuel_cost_options.append(fuel)

    return min(fuel_cost_options)


@aoc_output_formatter(2021, 7, 1, 'minimum fuel required to align crabs')
def part_one(crabs):
    basic_fuel_cost = lambda crab, position: abs(position - crab)
    return _determine_minimal_crab_fuel(crabs, basic_fuel_cost)


@aoc_output_formatter(2021, 7, 2, 'correct minimum fuel required to align crabs')
def part_two(crabs):
    # the real fuel cost is the sum of the sequence 1 ... N, where N is the number of steps
    # a crab submarine must move to reach the target position
    def _real_fuel_cost(crab, position):
        steps = abs(crab - position)
        return (steps*(steps + 1)) // 2

    return _determine_minimal_crab_fuel(crabs, _real_fuel_cost)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    crabs = [int(x) for x in get_input(input_file)[0].split(',')]

    part_one(crabs)
    part_two(crabs)

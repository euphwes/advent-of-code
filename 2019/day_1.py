from math import floor

from util.input import get_input
from util.decorators import aoc_output_formatter

DAY = 1
YEAR = 2019

PART_ONE_DESCRIPTION = "fuel requirements"
PART_ONE_ANSWER = 3361976

PART_TWO_DESCRIPTION = "improved fuel requirements"
PART_TWO_ANSWER = 5040085


# Expression for determining fuel requirements for a given mass
fuel_req = lambda mass: int(floor(mass / 3)) - 2


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(problem_input):

    # Simply sum the fuel requirements for each module mass.
    fuel_reqs = [fuel_req(mass) for mass in problem_input]
    return sum(fuel_reqs)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(problem_input):

    # Holds the components of all fuel requirements for the mission
    mission_fuel_reqs = list()

    for mass in problem_input:

        # Hold a list of component fuel requirements for this module, starting
        # with the fuel requirements for this module iself.
        module_fuel_reqs = [fuel_req(mass)]

        # Determine fuel reqs for the last element of the array (the most
        # recent chunk of fuel reqs calculated) and append it to the list.
        # Keep doing this until the new fuel reqs become 'negligible'
        while (new_fuel := fuel_req(module_fuel_reqs[-1])) >= 0:
            module_fuel_reqs.append(new_fuel)

        # Add the total fuel reqs for this module to the mission fuel reqs
        mission_fuel_reqs.append(sum(module_fuel_reqs))

    return sum(mission_fuel_reqs)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = [int(n) for n in get_input(input_file)]
    part_one(stuff)

    stuff = [int(n) for n in get_input(input_file)]
    part_two(stuff)

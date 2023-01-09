from dataclasses import dataclass
from enum import Enum
from typing import Set

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 12
YEAR = 2018

PART_ONE_DESCRIPTION = "sum of pot numbers with plants after 20 generations"
PART_ONE_ANSWER = 2952

PART_TWO_DESCRIPTION = "sum of pot numbers with plants after 50 billion generations"
PART_TWO_ANSWER = 4350000000957


@dataclass
class PottingRule:
    """Defines a rule that dictates whether a pot with a certain neighbor state will be alive or
    dead at the next iteration."""

    nearby_plants: Set[int]
    nearby_empties: Set[int]
    pot_result: str

    @staticmethod
    def from_line(line):
        """Parse a line from the problem input into a rule, which dictates which neighbors
        (relative to a pot position being checked) are alive or dead, and if the rule matches,
        whether the pot being checked will have a plant or not at the next iteration."""

        condition, outcome = line.split(" => ")

        # Hold the (relative) indices of nearby pots which either have plants or don't.
        nearby_plant_ixs = set()
        nearby_empty_ixs = set()

        # Example "condition":
        #    .##..
        #      ^
        #
        # The pot being checked is the middle one. Remember within +/- 2 pots of this pot,
        # whether that position contains a plant or is empty.
        for relative_ix, value in zip([-2, -1, 0, 1, 2], condition):
            if value == "#":
                nearby_plant_ixs.add(relative_ix)
            else:
                nearby_empty_ixs.add(relative_ix)

        return PottingRule(
            nearby_plants=nearby_plant_ixs,
            nearby_empties=nearby_empty_ixs,
            pot_result=outcome,
        )

    def matches(self, curr_ix, plant_locations):
        """For a given pot index, and state of which pots are occupied by plants, determine if
        the pot under investigation matches this rule."""

        matches = True

        for relative_ix in self.nearby_plants:
            nearby_ix = curr_ix + relative_ix
            if nearby_ix not in plant_locations:
                matches = False
                break

        for relative_ix in self.nearby_empties:
            nearby_ix = curr_ix + relative_ix
            if nearby_ix in plant_locations:
                matches = False
                break

        return matches


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(plant_info):
    # Read the first line of the input and see which pot indices start off holding plants.
    pots = plant_info.pop(0).replace("initial state: ", "")
    plant_locations = {ix for ix, plant in enumerate(pots) if plant == "#"}

    rules = [PottingRule.from_line(line) for line in plant_info if line]

    # For 20 generations...
    for _ in range(20):

        # Temporary holding place for the next generation of plants
        next_plant_locations = set()

        # For each relevant index: (2 below the minimum current potted plant, and 2 above,
        # because the rules check +/-2 from each pot you check), find the first matching rule.
        min_pot = min(plant_locations) - 2
        max_pot = max(plant_locations) + 3
        for ix in range(min_pot, max_pot):
            for rule in rules:

                # If the rule matches, AND the outcome for that rule is that the pot with that
                # index will have a plant at the next generation, at that pot index to the set
                # of indices of pots with plants next iteration.
                if (
                    rule.matches(curr_ix=ix, plant_locations=plant_locations)
                    and rule.pot_result == "#"
                ):
                    next_plant_locations.add(ix)
                    break

        plant_locations = next_plant_locations

    return sum(plant_locations)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two():

    fifty_billion = 50_000_000_000

    # By inspecting the state of the pots with plants after a large number of generations, I can
    # see that the system ends up with a statically-sized row of alternating empty and full pots
    # of plants that end up moving right by 1 unit every cycle.
    # Ex:
    # ............#.#.#.#.#.#.#.#...........
    # .............#.#.#.#.#.#.#.#..........
    # ..............#.#.#.#.#.#.#.#.........
    # ...............#.#.#.#.#.#.#.#........

    # After the pattern settles into this steeady state, I checked the ix of the
    # lowest-pot-number plant and the highest pot number plant and saw they matched this pattern
    min_plant = fifty_billion - 75
    max_plant = fifty_billion + 97

    return sum(range(min_plant, max_plant + 1, 2))


# ----------------------------------------------------------------------------------------------


def run(input_file):

    plant_info = get_input(input_file)

    part_one(plant_info)
    part_two()

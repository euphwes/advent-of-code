from itertools import combinations

from util.algs import manhattan_distance_4d
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 25
YEAR = 2018

PART_ONE_DESCRIPTION = "number of constellations formed by spacetime points"
PART_ONE_ANSWER = 314


def _parse_spacetime(spacetime_input):
    """Parse the problem input into a list of 4D points."""

    return [tuple(int(n) for n in line.split(",")) for line in spacetime_input]


def _point_belongs_to_constellation(point, constellation):
    """Given 1 point and a 'constellation' (a collection of points), return whether
    the first point belongs to the provided constellation because it's within 3 units
    of any of the other points in the constellation."""

    return any(
        manhattan_distance_4d(point, other_point) <= 3 for other_point in constellation
    )


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(spacetime_input):

    # Hold a list of constellations we find.
    constellations = []
    for point in _parse_spacetime(spacetime_input):
        added_to_existing_constellation = False

        # Check each of the constellations we currently know about, and see if the
        # point belongs to that constellation. If so, add it and then skip to the next
        # point.
        for constellation in constellations:
            if _point_belongs_to_constellation(point, constellation):
                constellation.append(point)
                added_to_existing_constellation = True
                break

        # If this point didn't belong to any existing constellations, start a new
        # constellation with this point.
        if not added_to_existing_constellation:
            constellations.append([point])

    # It's possible due to the order of spacetime points in the list that we recorded
    # multiple constellations which are in fact 1 larger constellation.
    while True:
        did_combine_constellations = False

        # For each combination of constellations...
        for con1, con2 in combinations(constellations, 2):

            # ... check if any of the points in constellation 1 also belong
            # to the second constellation.
            for point in con1:

                # If so, these points in fact just belong to 1 large constellation.
                # Remove all the points from constellation 2 and add them to the first.
                if _point_belongs_to_constellation(point, con2):
                    did_combine_constellations = True
                    while con2:
                        con1.append(con2.pop())
                    break

            # If we recorded that we did combine any constellations, rebuild the
            # list of constellations and remove any "empty" ones (because those points
            # were combined into another constellation). Then break into the outer loop
            # and start checking pairs of constellations again to see if they can be
            # further combined.
            if did_combine_constellations:
                constellations = [c for c in constellations if c]
                break

        # If we took a pass through all pairs of constellations and didn't find any that
        # could be combined, return the total number of constellations we found.
        if not did_combine_constellations:
            return len(constellations)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    spacetime_input = get_input(input_file)
    part_one(spacetime_input)

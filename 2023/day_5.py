from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

from math import inf as INFINITY

DAY = 5
YEAR = 2023

PART_ONE_DESCRIPTION = "lowest location corresponding to an initial seed (too few)"
PART_ONE_ANSWER = 331445006

PART_TWO_DESCRIPTION = "lowest location corresponding to an initial seed (full seeds)"
PART_TWO_ANSWER = 6472060


def _build_almanac_maps(almanac_except_seeds):
    """Build and return all the maps in the almanac, which map seed to soil numbers,
    soil to fertilizer numbers, etc."""

    seed_to_soil = list()
    soil_to_fert = list()
    fert_to_water = list()
    water_to_light = list()
    light_to_temp = list()
    temp_to_humid = list()
    humid_to_loc = list()

    maps = [
        seed_to_soil,
        soil_to_fert,
        fert_to_water,
        water_to_light,
        light_to_temp,
        temp_to_humid,
        humid_to_loc,
    ]
    curr_map = None

    # Keeping reading through the alamanac input line-by-line
    while almanac_except_seeds:
        line = almanac_except_seeds.pop(0)
        if not line:
            continue

        # If the word "map" is in the line, we've finished parsing all of the number ranges
        # mapped in the current line. Move on to the next map we need to parse.
        if "map" in line:
            curr_map = maps.pop(0)
            continue

        # Each line is 3 integers: the start of the destination range, the start of the source
        # range, and the size of both ranges.
        destination_start, source_start, size = (int(x) for x in line.split())

        # Append two tuples to the current map, the start and endpoints of both the start and
        # destination ranges.
        assert curr_map is not None
        curr_map.append(
            (
                (source_start, source_start + size - 1),
                (destination_start, destination_start + size - 1),
            )
        )

    # Return the list of maps in the order that they'll need to be evaluated when translating
    # from seed to location values.
    return [
        seed_to_soil,
        soil_to_fert,
        fert_to_water,
        water_to_light,
        light_to_temp,
        temp_to_humid,
        humid_to_loc,
    ]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(almanac):
    # Parse the list of seeds out of the first line of the puzzle input.
    line = almanac.pop(0)
    seeds = [int(x) for x in line.replace("seeds: ", "").split()]

    maps = _build_almanac_maps(almanac)

    # For every seed, follow it through all the maps to find the corresponding location.
    # Keep track of the minimum location.
    minimum_location = INFINITY
    for value in seeds:
        for mmap in maps:
            for s_range, d_range in mmap:
                if value >= s_range[0] and value <= s_range[1]:
                    ix = value - s_range[0]
                    value = d_range[0] + ix
                    break
        minimum_location = min([value, minimum_location])

    return minimum_location


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(almanac):
    # Parse a list of (range_start, range_size) tuples for seed values out of the first line
    # of the puzzle input.
    line = almanac.pop(0)
    seeds = [int(x) for x in line.replace("seeds: ", "").split()]

    seed_ranges = list()
    while seeds:
        start_seed = seeds.pop(0)
        range_size = seeds.pop(0)
        seed_ranges.append((start_seed, start_seed + range_size - 1))

    def _does_seed_exist(target_seed):
        """Helper function for determining if a given seed is inside any of the ranges
        of initial seeds defined by the puzzle input."""
        for sr_start, sr_end in seed_ranges:
            if sr_start <= target_seed and target_seed <= sr_end:
                return True
        return False

    # Parse the almanac and get the seed-to-soil-to-fertilizer-to...-to-location maps.
    # Sort the humidity-to-location map by the starting value of the location ranges, from
    # low to high, because we're going to iterate over all possible locations, lowest to highest
    maps = _build_almanac_maps(almanac)
    humid_to_loc = maps[-1]
    sorted_locations = sorted(humid_to_loc, key=lambda x: x[1][0])

    # For each location range...
    for _, loc_range in sorted_locations:
        # ... for every location in that range...
        for value in int_stream(loc_range[0], loc_range[1]):
            # Remember the starting location, and then follow the location value all the way
            # through the maps until we get to a seed value.
            init_loc = value
            for mmap in reversed(maps):
                for s_range, d_range in mmap:
                    if value >= d_range[0] and value <= d_range[1]:
                        ix = value - d_range[0]
                        value = s_range[0] + ix
                        break

            # If this is a valid seed from the
            if _does_seed_exist(value):
                return init_loc


# ----------------------------------------------------------------------------------------------


def run(input_file):
    almanac = get_input(input_file)
    part_one(almanac)

    almanac = get_input(input_file)
    part_two(almanac)

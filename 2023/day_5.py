from functools import lru_cache
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 5
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = 331445006

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = 6472060


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    seeds = list()

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

    line = stuff.pop(0)
    if "seeds:" in line:
        seeds = [int(x) for x in line.replace("seeds: ", "").split()]
    stuff.pop(0)

    curr_map = list()
    while stuff:
        line = stuff.pop(0)
        if not line:
            continue
        if "map" in line:
            curr_map = maps.pop(0)
            continue

        d_start, s_start, size = (int(x) for x in line.split())
        curr_map.append(((s_start, s_start + size - 1), (d_start, d_start + size - 1)))

    maps = [
        seed_to_soil,
        soil_to_fert,
        fert_to_water,
        water_to_light,
        light_to_temp,
        temp_to_humid,
        humid_to_loc,
    ]

    locations = list()
    for s in seeds:
        init = s
        for mmap in maps:
            for s_range, d_range in mmap:
                if s >= s_range[0] and s <= s_range[1]:
                    ix = s - s_range[0]
                    s = d_range[0] + ix
                    break
        locations.append(s)
        # print(f"{init} goes to {s}")

    return min(locations)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    seeds = list()

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

    line = stuff.pop(0)
    if "seeds:" in line:
        seeds = [int(x) for x in line.replace("seeds: ", "").split()]
    stuff.pop(0)

    curr_map = list()
    while stuff:
        line = stuff.pop(0)
        if not line:
            continue
        if "map" in line:
            curr_map = maps.pop(0)
            continue

        d_start, s_start, size = (int(x) for x in line.split())
        curr_map.append(((s_start, s_start + size - 1), (d_start, d_start + size - 1)))

    maps = [
        seed_to_soil,
        soil_to_fert,
        fert_to_water,
        water_to_light,
        light_to_temp,
        temp_to_humid,
        humid_to_loc,
    ]

    seed_ranges = list()
    while seeds:
        s1 = seeds.pop(0)
        s2 = seeds.pop(0)
        seed_ranges.append((s1, s1 + s2 - 1))

    def _does_seed_exist(target_seed):
        for sr_start, sr_end in seed_ranges:
            if sr_start <= target_seed and target_seed <= sr_end:
                return True
        return False

    sorted_locs = sorted(humid_to_loc, key=lambda x: x[1][0])
    for _, loc_range in sorted_locs:
        for loc in int_stream(loc_range[0], loc_range[1]):
            init_loc = loc
            for mmap in reversed(maps):
                for s_range, d_range in mmap:
                    if loc >= d_range[0] and loc <= d_range[1]:
                        ix = loc - d_range[0]
                        loc = s_range[0] + ix
                        break
            if _does_seed_exist(loc):
                return init_loc


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

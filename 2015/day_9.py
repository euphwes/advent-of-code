from itertools import permutations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 9
YEAR = 2015

PART_ONE_DESCRIPTION = "distance of shortest route"
PART_ONE_ANSWER = 251

PART_TWO_DESCRIPTION = "distance of shortest route"
PART_TWO_ANSWER = 898


def _parse_city_distance(line: str) -> tuple[tuple[str, str], int]:
    """Parse distance between cities in a line of the problem input.

    Returns a tuple of (city A, city B) and their distance.
    Ex: "AlphaCentauri to Straylight = 133" --> ((AlphaCentauri, Straylight), 133)
    """
    tokens = line.split()
    return ((tokens[0], tokens[2]), int(tokens[4]))


def _brute_force_route_lengths(
    cities: set[str],
    distance_map: dict[tuple[str, str], int],
) -> list[tuple[list[str], int]]:
    """Calculate the route length of every possible route through the cities provided.

    Returns a list of tuples, which is a list of cities visited, and the total route length
    when visiting the cities in that order.
    """

    distances = []
    for city_list in permutations(cities):
        distance = 0
        for i in range(len(city_list) - 1):
            city1, city2 = city_list[i], city_list[i + 1]
            distance += distance_map[(city1, city2)]
        distances.append((city_list, distance))

    return distances


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    # Parse each line into a tuple of (city1, city2) and distance
    city_distances = [_parse_city_distance(line) for line in raw_input]

    # Hold the distinct cities we know about, as well as the distance between each pair
    cities = set()
    city_distance_map = {}

    # Iterate the city distances and put the pairs of cities into a map with their distance.
    # Put the pairs in both orders so we can look them up either way.
    for (city1, city2), distance in city_distances:
        city_distance_map[(city1, city2)] = distance
        city_distance_map[(city2, city1)] = distance
        cities.add(city1)
        cities.add(city2)

    return min(
        route_len for _, route_len in _brute_force_route_lengths(cities, city_distance_map)
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    # Parse each line into a tuple of (city1, city2) and distance
    city_distances = [_parse_city_distance(line) for line in raw_input]

    # Hold the distinct cities we know about, as well as the distance between each pair
    cities = set()
    city_distance_map = {}

    # Iterate the city distances and put the pairs of cities into a map with their distance.
    # Put the pairs in both orders so we can look them up either way.
    for (city1, city2), distance in city_distances:
        city_distance_map[(city1, city2)] = distance
        city_distance_map[(city2, city1)] = distance
        cities.add(city1)
        cities.add(city2)

    return max(
        route_len for _, route_len in _brute_force_route_lengths(cities, city_distance_map)
    )


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from itertools import permutations

#---------------------------------------------------------------------------------------------------

def __parse_city_distance(tokens):
    """ For a given list of tokens [City1, "to", City2, "=", distance], returns a tuple of the two
    cities and their distance: ((City1, City2), distance). """

    return ((tokens[0], tokens[2]), int(tokens[4]))


def __brute_force_route_lengths(cities, distance_map):
    """ Calculates the route length of every possible route through the cities provided. Returns a
    list of tuples of (city_list, route_length). """

    distances = list()
    for city_list in permutations(cities):
        distance = 0
        for i in range(len(city_list) - 1):
            city1, city2 = city_list[i], city_list[i+1]
            distance += distance_map[(city1, city2)]
        distances.append((city_list, distance))

    return distances

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 9, 1, 'distance of shortest route', assert_answer=251)
def part_one(cities, city_distance_map):
    return min(route_len for _, route_len in __brute_force_route_lengths(cities, city_distance_map))


@aoc_output_formatter(2015, 9, 2, 'distance of longest route', assert_answer=898)
def part_two(cities, city_distance_map):
    return max(route_len for _, route_len in __brute_force_route_lengths(cities, city_distance_map))

#---------------------------------------------------------------------------------------------------

def run(input_file):

    # Parse each line into a tuple of (city1, city2) and distance
    city_distances = [__parse_city_distance(line) for line in get_tokenized_input(input_file, ' ')]

    # Hold the distinct cities we know about, as well as the distance between each pair
    cities = set()
    city_distance_map = dict()

    # Iterate the city distances and put the pairs of cities into a map with their distance.
    # Put the pairs in both orders so we can look them up either way.
    for (city1, city2), distance in city_distances:
        city_distance_map[(city1, city2)] = distance
        city_distance_map[(city2, city1)] = distance
        cities.add(city1)
        cities.add(city2)

    part_one(cities, city_distance_map)
    part_two(cities, city_distance_map)

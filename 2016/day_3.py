from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 3
YEAR = 2016

PART_ONE_DESCRIPTION = "possible triangles"
PART_ONE_ANSWER = 1032

PART_TWO_DESCRIPTION = "possible triangles"
PART_TWO_ANSWER = 1838


def _is_possible_triangle(side_lengths):
    s1, s2, s3 = side_lengths
    return (s1 + s2 > s3) and (s2 + s3 > s1) and (s1 + s3 > s2)


@aoc_output_formatter(2016, 3, 1, "possible triangles")
def part_one(potential_triangles):
    return sum([1 for tri in potential_triangles if _is_possible_triangle(tri)])


@aoc_output_formatter(2016, 3, 2, "possible triangles")
def part_two(potential_triangles):
    return sum([1 for tri in potential_triangles if _is_possible_triangle(tri)])


# ----------------------------------------------------------------------------------------------


def run(input_file):

    potential_triangles = list()
    for line in get_input(input_file):
        s1, s2, s3 = int(line[:3]), int(line[3:8]), int(line[8:])
        potential_triangles.append((s1, s2, s3))

    part_one(potential_triangles)

    potential_triangles = list()
    tri1, tri2, tri3 = list(), list(), list()
    for line in get_input(input_file):
        s1, s2, s3 = int(line[:3]), int(line[3:8]), int(line[8:])
        tri1.append(s1)
        tri2.append(s2)
        tri3.append(s3)
        if len(tri1) == 3:
            potential_triangles.append(tri1)
            potential_triangles.append(tri2)
            potential_triangles.append(tri3)
            tri1, tri2, tri3 = list(), list(), list()

    part_two(potential_triangles)

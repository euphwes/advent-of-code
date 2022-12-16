from itertools import permutations

from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

DAY = 13
YEAR = 2015

PART_ONE_DESCRIPTION = "Max happiness"
PART_ONE_ANSWER = 733

PART_TWO_DESCRIPTION = "Max happiness with me included"
PART_TWO_ANSWER = 725


def _parse_happiness(tokens):
    """Parses an input line and determines how much happiness person1 would gain/lose by sitting
    next to person2. Returns the parsed input line as ((person1, person2), happiness_person1).

    Ex: Alice would gain 2 happiness units by sitting next to Bob."""

    return (
        (tokens[0], tokens[-1][0:-1]),
        int(tokens[3]) * (1 if tokens[2] == "gain" else -1),
    )


def _evaluate_seating_chart(seating_chart, happiness_map):
    """Evaluates a 'seating chart' of people and determines their overall happiness."""

    happiness = 0
    for i, person1 in enumerate(seating_chart):
        person2 = seating_chart[(i + 1) % len(seating_chart)]
        happiness += happiness_map[(person1, person2)]
        happiness += happiness_map[(person2, person1)]

    return happiness


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(people, happiness_map):
    return max(
        _evaluate_seating_chart(chart, happiness_map) for chart in permutations(people)
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(people, happiness_map):
    return max(
        _evaluate_seating_chart(chart, happiness_map) for chart in permutations(people)
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):

    # Parse each line into a tuple of ((person1, person2) ,hapiness_person1), and then into a
    # dict mapping each pair of people to the happiness change for person1
    happiness_pairs = [
        _parse_happiness(line) for line in get_tokenized_input(input_file, " ")
    ]
    happiness_map = {people: happiness for people, happiness in happiness_pairs}

    # Determine each distinct person
    people = list(set(people_pair[0] for people_pair in happiness_map.keys()))

    part_one(people, happiness_map)

    # Oops, you forgot yourself. Add yourself to the list with a 0 score for all pairings.
    for person in people:
        happiness_map[("me", person)] = 0
        happiness_map[(person, "me")] = 0
    people.append("me")

    part_two(people, happiness_map)

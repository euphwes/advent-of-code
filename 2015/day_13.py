from itertools import permutations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 13
YEAR = 2015

PART_ONE_DESCRIPTION = "Max happiness"
PART_ONE_ANSWER = 733

PART_TWO_DESCRIPTION = "Max happiness with me included"
PART_TWO_ANSWER = 725


def _parse_happiness(tokens: list[str]) -> tuple[tuple[str, str], int]:
    """Determine the happiness person #1 gains by sitting next to person #2.

    Parse an input line and determines how much happiness person1 would gain/lose by sitting
    next to person2. Returns the parsed input line as ((person1, person2), happiness_person1).

    Ex: Alice would gain 2 happiness units by sitting next to Bob.
    --> (("Alice", "Bob"), 2)
    """

    return (
        (tokens[0], tokens[-1][0:-1]),
        int(tokens[3]) * (1 if tokens[2] == "gain" else -1),
    )


def _parse_happiness_map(raw_input: list[str]) -> dict[tuple[str, str], int]:
    """Build a map of the happiness of people sitting next to other people.

    Accepts the problem raw input, and returns dictionary of people pairs to the happiness that
    the first person would gain sitting next to the 2nd person.
    """

    happiness_pairs = [_parse_happiness(line.split()) for line in raw_input]
    return dict(happiness_pairs)


def _evaluate_seating_chart(
    seating_chart: tuple[str, ...],
    happiness_map: dict[tuple[str, str], int],
) -> int:
    """Evaluate the total happiness of a 'seating chart'.

    Accepts an ordered arrangement of people, and a mapping of the happiness of every pair of
    people, and returns the sum of the happiness of each person.
    """

    happiness = 0
    for i, person1 in enumerate(seating_chart):
        person2 = seating_chart[(i + 1) % len(seating_chart)]
        happiness += happiness_map[(person1, person2)]
        happiness += happiness_map[(person2, person1)]

    return happiness


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    happiness_map = _parse_happiness_map(raw_input)
    people = {people_pair[0] for people_pair in happiness_map}

    return max(_evaluate_seating_chart(chart, happiness_map) for chart in permutations(people))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    happiness_map = _parse_happiness_map(raw_input)
    people = {people_pair[0] for people_pair in happiness_map}

    # Oops, you forgot yourself. Add yourself to the list with a 0 score for all pairings.
    for person in people:
        happiness_map[("me", person)] = 0
        happiness_map[(person, "me")] = 0
    people.add("me")

    return max(_evaluate_seating_chart(chart, happiness_map) for chart in permutations(people))


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

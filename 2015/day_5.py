from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 5
YEAR = 2015

PART_ONE_DESCRIPTION = "nice strings (v1)"
PART_ONE_ANSWER = 258

PART_TWO_DESCRIPTION = "nice strings (v2)"
PART_TWO_ANSWER = 53


VOWELS = set("aeiou")
FORBIDDEN_LETTER_PAIRS = {"ab", "cd", "pq", "xy"}


def _contains_three_vowels(target: str) -> bool:
    """Return if a string contains at least 3 vowels."""

    return len([c for c in target if c in VOWELS]) >= 3


def _vet_letter_pairs(target: str) -> bool:
    """Return if a string contains a valid letter pair.

    A valid letter pair is a letter repeated twice anywhere in the string, and is not one of
    a predetermined set of forbidden letter pairs.
    """

    found_double_letters = False

    for i in range(len(target) - 1):
        substring = target[i : i + 2]

        if substring in FORBIDDEN_LETTER_PAIRS:
            return False

        if len(list(set(substring))) == 1:
            found_double_letters = True

    return found_double_letters


def _has_double_letter_pairs(target: str) -> bool:
    """Return if a string has two pairs of the same letter which don't overlap."""

    pairs = {}

    for i in range(len(target) - 1):
        substring = target[i : i + 2]

        if substring in pairs:
            indices = pairs[substring]
            for j in indices:
                if i >= (j + 2):
                    return True

            indices.append(i)
            pairs[substring] = indices

        else:
            pairs[substring] = [i]

    return False


def _has_letter_sandwich(target: str) -> bool:
    """Return if a string contains a "letter sandwich".

    A letter sandwich is when one letter repeats with exactly one different letter
    between them. Ex: aba, eje, kmk
    """

    for i in range(len(target) - 2):
        substring = target[i : i + 3]
        if substring[0] == substring[-1]:
            return True

    return False


def _is_nice_v1(target: str) -> bool:
    """Determine if a string is "nice", which requires it to meet three criteria.

    1. contains at least 3 vowels (aeiou)
    2. contains at least 1 letter twice in a row
    3. does not contain the strings ab, cd, pq, or xy
    """

    return _contains_three_vowels(target) and _vet_letter_pairs(target)


def _is_nice_v2(target: str) -> bool:
    """Determine if a string is "nice", which requires it to meet two criteria.

    1. contains a pair of letters that appears at least twice in the string without overlapping
    2. contains at least one letter which repeats with exactly one letter between them
    """

    return _has_letter_sandwich(target) and _has_double_letter_pairs(target)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return sum(1 if _is_nice_v1(s) else 0 for s in raw_input)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    return sum(1 if _is_nice_v2(s) else 0 for s in raw_input)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

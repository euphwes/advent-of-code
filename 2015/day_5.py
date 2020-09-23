from util.decorators import aoc_output_formatter
from util.input import get_input

from hashlib import md5

#---------------------------------------------------------------------------------------------------

def __contains_three_vowels(target):
    """ Returns if a string contains at least 3 vowels. """

    is_vowel = lambda c: c in list('aeiou')
    return sum(1 if is_vowel(c) else 0 for c in target) >= 3


def __vet_letter_pairs(target):
    """ Returns true if string contains a letter repeated twice anywhere in the string, and does not
    contain a forbidden pair anywhere. """

    is_forbidden = lambda pair: pair in ['ab', 'cd', 'pq', 'xy']
    is_double_letter = lambda pair: len(set(list(pair))) == 1

    found_double_letters = False

    for i in range(0, len(target) - 1):
        substring = target[i : i + 2]

        if is_forbidden(substring):
            return False

        if is_double_letter(substring):
            found_double_letters = True

    return found_double_letters


def __has_double_letter_pairs(target):
    """ Determines if a string has two pairs of the same letter which don't overlap. """

    pairs = dict()

    for i in range(0, len(target) - 1):
        substring = target[i : i + 2]

        if substring in pairs.keys():
            indices = pairs[substring]
            for j in indices:
                if i >= (j + 2):
                    return True

            indices.append(i)
            pairs[substring] = indices

        else:
            pairs[substring] = [i]

    return False


def __has_letter_sandwich(target):
    """ Determines if a string has a least one letter which repeats with exactly one letter between
    them. """

    for i in range(0, len(target) - 2):
        substring = target[i : i + 3]
        if substring[0] == substring[-1]:
            return True

    return False


def __is_nice_v1(target):
    """ Determines if a string is "nice", which requires it to meet three criteria:
    1. contains at least 3 vowels (aeiou)
    2. contains at least 1 letter twice in a row
    3. does not contain the strings ab, cd, pq, or xy """

    return __contains_three_vowels(target) and __vet_letter_pairs(target)


def __is_nice_v2(target):
    """ Determines if a string is "nice", which requires it to meet two criteria:
    1. contains a pair of two letters that appears at least twice in the string without overlapping
    2. contains at least one letter which repeats with exactly one letter between them """

    return __has_letter_sandwich(target) and __has_double_letter_pairs(target)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 5, 1, 'nice strings (v1)')
def part_one(strings):
    return sum(1 if __is_nice_v1(s) else 0 for s in strings)


@aoc_output_formatter(2015, 5, 2, 'nice strings (v2)')
def part_two(strings):
    return sum(1 if __is_nice_v2(s) else 0 for s in strings)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    strings = get_input(input_file)

    part_one(strings)
    part_two(strings)

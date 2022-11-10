from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from collections import Counter

#---------------------------------------------------------------------------------------------------

def _is_valid_v1(phrase):
    """ A phrase is valid if no words are repeated. """

    return len(phrase) == len(set(phrase))


def _is_valid_v2(phrase):
    """ A phrase is valid if no words are anagrams of another. """

    word_counters = list()
    for word in phrase:
        letter_counts = Counter(word)

        # If this counter of letters in the word already matches another word whose
        # letters have been counted, this is an anagram and the passphrase is invalid.
        if letter_counts in word_counters:
            return False
        else:
            word_counters.append(letter_counts)

    return True


def _count_valid_passphrases(passphrases, validity_checker):
    """ Returns a count of valid passphrases in the list, as evaluated by the provided
    validity checker function. """

    return sum(1 if validity_checker(phrase) else 0 for phrase in passphrases)


@aoc_output_formatter(2017, 4, 1, 'number of valid passphrases')
def part_one(passphrases):
    return _count_valid_passphrases(passphrases, _is_valid_v1)


@aoc_output_formatter(2017, 4, 2, 'number of valid (v2) passphrases')
def part_two(passphrases):
    return _count_valid_passphrases(passphrases, _is_valid_v2)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    passphrases = get_tokenized_input(input_file, None)

    part_one(passphrases)
    part_two(passphrases)

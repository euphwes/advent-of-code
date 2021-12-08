from itertools import permutations

from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

# Reference for "segment index" of each segment in seven-segment display
#
#     0000
#    1    2
#    1    2
#     3333
#    4    5
#    4    5
#     6666

# Map digits to which segments are on when that digit is being displayed.
digit_segment_id_map = {
    0: [0, 1, 2, 4, 5, 6],
    1: [2, 5],
    2: [0, 2, 3, 4, 6],
    3: [0, 2, 3, 5, 6],
    4: [1, 2, 3, 5],
    5: [0, 1, 3, 5, 6],
    6: [0, 1, 3, 4, 5, 6],
    7: [0, 2, 5],
    8: [0, 1, 2, 3, 4, 5, 6],
    9: [0, 1, 2, 3, 5, 6]
}


def _build_digit_signal_map_from_candidate(candidate):
    """ For a given "signal set arrangment" candidate (which signal letters correspond to which
    segment IDs), build and return a map which says which signals are on for a given digit to
    be displayed.

    Ex: candidate = "gfedbca" means...
        segment 0's signal is g
        segment 1's signal is f
        ...
        segment 6's signal is a

    Return a map for each digit 0-9 which specifies which signals are on, in order to light up
    the segments to display that digit.

    Returns {
        0: set('abcefg'),
        7: set('geb'),
        # etc
    }
    """

    # Holds the map of digit to which signals are on for it to be displayed.
    digit_signal_map = dict()

    # Iterate each digit and which segment IDs are on for it
    for digit, segments in digit_segment_id_map.items():
        # Determine which signals are on for each segment displayed for this digit.
        digit_signal_map[digit] = {candidate[n] for n in segments}

    return digit_signal_map


def _deduce_signals_map(seed_digit_signal_map, signals):
    """ For a given "seed" digit to signal map, which maps the digits [1, 4, 7] to a set of which
    signals are on to display them, and a set of all signals seen for this display, deduce and
    return a complete signals-to-digit map for all digits 0-9. """

    # There aren't that many permutations of 7 items. Try all of them.
    # Each permutation here is an arrangment of the signals a-g, and the order in which they appear
    # indicates the index of the seven segment ID (see ascii art above) that signal corresponds to.
    # abcdefg indicates the following segment ID to signal mappings:
    #    0: a
    #    1: b
    #    2: c
    for perm in permutations('abcdefg', 7):
        # Figure out what sets of signals are on for digits 1, 4, and 7 for this permutation.
        # We can bail on a permutation early if the signal sets for digits 1, 4, and 7 don't match
        # what we already previously determined.
        if not all([
            {perm[n] for n in digit_segment_id_map[1]} == seed_digit_signal_map[1],
            {perm[n] for n in digit_segment_id_map[4]} == seed_digit_signal_map[4],
            {perm[n] for n in digit_segment_id_map[7]} == seed_digit_signal_map[7]
        ]):
            continue

        # If we've gotten this far, this signal/segment permutation might be correct.
        # Build a map of digits to sets of signals which are on to display that digit.
        candidate_digit_to_signal_map = _build_digit_signal_map_from_candidate(perm)

        # If this is the correct complete map of numbers to signals, all signals in the input
        # will be present in this map's keys.
        if all(signal in candidate_digit_to_signal_map.values() for signal in signals):
            # This is the correct map. Flip it to turn it into a map of signals to digits.
            return { _normalize(s): d for d, s in candidate_digit_to_signal_map.items() }

    # If we got here, I did something wrong because we couldn't deduce which signal sets correspond
    # to which digits.
    raise Exception("Couldn't find solution for digit to signal set map.")


def _build_seed_digit_to_signals_map(signals):
    """ Since digits 1, 4, and 7 have a unique number of segments lit up, we can determine if a
    signal set corresponds to one of these digits by the length of the signal set. Check the signals
    and build a map of digits 1, 4, 7 to which signal sets represent them. """

    digit_map = {}
    for signal_set in signals:
        signal_length = len(signal_set)
        if signal_length == 2:
            digit_map[1] = signal_set
        elif signal_length == 3:
            digit_map[7] = signal_set
        elif signal_length == 4:
            digit_map[4] = signal_set
        elif signal_length == 7:
            digit_map[8] = signal_set

    return digit_map


def _normalize(signal):
    """ Sets aren't hashable, so we need to turn a set of signals back into a predictable string
    before we can use a chunk of signals as the key in a map. Take the signal set, sort by
    alphabetical order and join all the signal letters into a single string.

    Ex: set('dgab') -> 'abdg'
    """
    return ''.join(sorted(list(signal)))


@aoc_output_formatter(2021, 8, 1, 'number of times digits 1,4,7,8 appear')
def part_one(outputs):
    count = 0
    for outs in outputs:
        # In seven-segment displays, digits 1, 4, 7, 8 have a distinct number of segments lit up.
        # 2, 4, 3, and 7 segments are lit respectively. If the length of signals in the output
        # are one of these values, we know we're seeing a digit 1, 4, 7, or 8.
        count += sum(1 for signal in outs if len(signal) in [2, 3, 4, 7])
    return count


@aoc_output_formatter(2021, 8, 2, '')
def part_two(signals, outputs):
    output_sum = 0

    for sigs, outs in list(zip(signals, outputs)):
        # For this row of signals, deduce which sets of signals correpond to which digits.
        seed_digit_map = _build_seed_digit_to_signals_map(sigs)
        signal_to_digit_map = _deduce_signals_map(seed_digit_map, sigs)

        # Now that we know what signals correspond to what digits, figure out what numbers
        # the outputs are displaying.
        output_digits = ''
        for output_signal in outs:
            output_digits += str(signal_to_digit_map[_normalize(output_signal)])

        # Turn those output digits into a number and add it to the running sum.
        output_sum += int(output_digits)
    return output_sum

#---------------------------------------------------------------------------------------------------

def run(input_file):

    lines = [line for line in get_input(input_file)]

    outputs_workspace = list()
    signals_workspace = list()

    for line in lines:
        split = line.split(' | ')
        signal, out = split[0], split[1]
        outputs_workspace.append(out)
        signals_workspace.append(signal)

    outputs = [[set(o) for o in out.split(' ')] for out in outputs_workspace]
    signals = [[set(s) for s in signal.split(' ')] for signal in signals_workspace]

    part_one(outputs)
    part_two(signals, outputs)

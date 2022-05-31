from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

from hashlib import md5
_md5 = lambda x: md5(x.encode()).hexdigest()

#---------------------------------------------------------------------------------------------------

def _contains_char_n_times(test, n, char=None):
    """ Checks if the test string provided contains `n` of the same character in a row.
    If a particular character is specified, this searches for that character and returns True or
    False depending on if that character is found `n` times in a row.

    If no character is specified, this checks all characters. If any n-tuples are found, this
    returns (True, <character>) for the first character which appears `n` times in a row. If no
    n-tuples are found, this returns (False, None). """

    if char is not None:
        for i in range(len(test)-n+1):
            if len(set(test[i:i+n])) == 1 and test[i] == char:
                return True
        return False

    else:
        for i in range(len(test)-n+1):
            if len(set(test[i:i+n])) == 1:
                return True, test[i]
        else:
            return False, None


def _determine_index_for_64th_key(hash_func):
    """ Using the provided hash function, calculate the hash at each index and determine which index
    produces the 64th key hash. """

    # Hold the indices of hashes which we know are keys.
    key_indices = set()

    # Map indices to triple character, for hashes which *might* be keys.
    key_candidates = dict()

    for n in int_stream(0):
        hash = hash_func(n)

        if n-1001 in key_candidates.keys():
            del key_candidates[n-1001]

        # If this hash doesn't have any triple at all, it can't be a key candidate, nor can it be
        # the 5-tuple verification of a prior key candidate in the past thousand hashes.
        has_triple, char = _contains_char_n_times(hash, 3, char=None)
        if not has_triple:
            continue

        # If this hash has a triple, remember the index of this hash and what the triple char was
        key_candidates[n] = char

        # Check the key candidates within the previous 1000 hashes to see if this one is a 5-tuple
        # verification of any of the previous key candidates. If so, those candidates are actual
        # keys, so we store those key indices.
        keys_to_remove = set()
        for ix in [ix for ix in key_candidates.keys() if ix < n and ix >= (n-1000)]:
            test_char = key_candidates[ix]
            if _contains_char_n_times(hash, 5, char=test_char):
                key_indices.add(ix)
                keys_to_remove.add(ix)

            # This part is a little hack-ish: we are specifically looking for the 64th key, but we
            # might need to find more than 64 because a later hash could potentially verify an
            # earlier candidate than one before it.
            #
            # Ex:
            #    hash at index 5010 could verify the candidate hash at index 4510, but...
            #    hash at index 5011 could verify the candidate hash at index 4011
            #
            # hash@4011 might be the 70th hash we identify as a key, but it's the 64th hash
            # calculated.
            #
            # Let's find more than the 64 minimum we need, and then sort the indices and pull the
            # 64th one. For my particular input, finding 70 keys is enough.
            if len(key_indices) == 70:
                return sorted(list(key_indices))[63]

        # Remove the newly-verified keys as candidates so we don't check those again.
        for ix in keys_to_remove:
            del key_candidates[ix]


@aoc_output_formatter(2016, 14, 1, 'index of the 64th one-time key')
def part_one(salt):

    hash_func = lambda n: _md5(salt + str(n))
    return _determine_index_for_64th_key(hash_func)


@aoc_output_formatter(2016, 14, 2, 'index of the 64th one-time key using key stretching')
def part_two(salt):

    def hash_func(n):
        hash = _md5(salt + str(n))
        for _ in range(2016):
            hash = _md5(hash)
        return hash

    return _determine_index_for_64th_key(hash_func)


#---------------------------------------------------------------------------------------------------

def run(input_file):

    salt = get_input(input_file)[0]

    part_one(salt)
    part_two(salt)

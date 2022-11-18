from functools import reduce

_xor = lambda x, y: x ^ y

def _rotate(sequence, steps):
    """ Rotates a sequence by N steps, wrapping elements back to the beginning. """

    steps = steps % len(sequence)
    return sequence[-steps:] + sequence[:-steps]


def knot_hash(bytes_to_hash, iterations=1):
    """ Performs `iterations` of Knot Hash on the provided input bytes and returns the result. """

    skip_size = 0
    current_pos = 0
    hashed = list(range(0, 256))

    for _ in range(iterations):
        for byte_value in bytes_to_hash:
            # Rather than attempting to reverse a chunk of the hashed values in a circular list
            # manner, rotate the hashed bytes by `current_pos` so we're always reversing the
            # chunk at the beginning, and then rotate the hashed values back.
            hashed = _rotate(hashed, -1 * current_pos)
            hashed = list(reversed(hashed[:byte_value])) + hashed[byte_value:]
            hashed = _rotate(hashed, current_pos)

            current_pos += (byte_value + skip_size) % 256
            skip_size += 1

    return hashed


def build_dense_hex_hash(sparse_hash):
    """ Returns a dense hash from a given sparse Knot hash.

    The sparse hash is always 256 bytes long. Each byte of the dense hash is calculated by
    performing bitwise XOR operations on the 16-byte chunks of the sparse hash.

    The final result is represented as a hexadecimal string. """

    _hex = lambda byte: hex(byte)[2:].zfill(2)

    dense_hash = list()
    for _ in range(16):
        dense_hash.append(reduce(_xor, sparse_hash[:16]))
        sparse_hash = sparse_hash[16:]

    return ''.join(map(_hex, dense_hash))

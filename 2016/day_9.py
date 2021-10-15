from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

COMPRESSION_MARKER_START = '('
COMPRESSION_MARKER_STOP  = ')'

#---------------------------------------------------------------------------------------------------

def _extract_compression_data(file_iter):
    """ Eats through a compressed file iterator and returns the compression marker info, a tuple
    of the form (next_count, number_times_to_repeat). """

    # Extract the rest of the compression marker
    buffer = ''
    while (next_char := next(file_iter)) != COMPRESSION_MARKER_STOP:
        buffer += next_char

    # The compression marker is of the form "{next_count}x{times_to_repeat}"
    next_count, repeat_times = buffer.split('x')
    next_count = int(next_count)
    repeat_times = int(repeat_times)

    return (next_count, repeat_times)


def _decompress_file_v2_len(compressed_file):
    """ Return the length of the decompressed file using the v2 experimental compression format. """

    # Base case of the recursive call -- no markers (stuff in parentheses) means the length
    # of the decompressed data is just the length of the data itself.
    if COMPRESSION_MARKER_START not in compressed_file:
        return len(compressed_file)

    decompressed_length = 0
    file_iter = iter(compressed_file)

    try:
        while True:
            # Keep popping characters off
            next_char = next(file_iter)

            # If the character isn't inside a compression marker, bump the decompressed length
            if next_char != COMPRESSION_MARKER_START:
                decompressed_length += 1

            # Once we hit a compression marker...
            else:
                # Extract the compression info from the marker
                next_count, repeat_times = _extract_compression_data(file_iter)
                # Pull the following chunk of compressed data
                compressed_data = [next(file_iter) for _ in range(next_count)]
                # Decompressed the compressed data and get its length, multiply that by the number
                # of times to repeat it, and add it to the decompressed length
                decompressed_length += (repeat_times * _decompress_file_v2_len(compressed_data))

    except StopIteration:
        return decompressed_length


def _decompress_file_v1(compressed_file):
    """ Decompress the file using the experimental compression format. """

    decompressed = list()
    file_iter = iter(compressed_file)

    try:
        while True:
            # Keep popping characters off
            next_char = next(file_iter)

            # If we're not inside a compression marker, add the character to the decompressed data
            if next_char != COMPRESSION_MARKER_START:
                decompressed.append(next_char)

            # If we hit a decompression marker...
            else:
                # Extract the compression info from the marker
                next_count, repeat_times = _extract_compression_data(file_iter)
                # Pull the following chunk of compressed data
                compressed_data = [next(file_iter) for _ in range(next_count)]
                # Then repeat the compressed data the specified number of times, adding it to the
                # decompressed data
                for _ in range(repeat_times):
                    decompressed.extend(compressed_data)

    except StopIteration:
        return ''.join(decompressed)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2016, 9, 1, 'length of decompressed file')
def part_one(compressed_file):
    return len(_decompress_file_v1(compressed_file))

@aoc_output_formatter(2016, 9, 2, 'length of v2 decompressed file')
def part_two(compressed_file):
    return _decompress_file_v2_len(compressed_file)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    compressed_file = get_input(input_file)[0]

    part_one(compressed_file)
    part_two(compressed_file)

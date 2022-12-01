from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def rotate_pattern(pattern):
    """ Rotate the provided pattern by 90 degrees clockwise and returns it.
    
    Ex:     . . .         # . .
            . # #   -->   . # .
            # . .         . # .
    """
    
    size = len(pattern)
    swapped_dict = dict()
    
    # First build a dictionary (coord to element) of the pattern flipped across the x=y line
    for y, line in enumerate(pattern):
        for x, element in enumerate(line):
            swapped_dict[(y, x)] = element
    
    # Turn the dictionary back into a list of strings
    swapped = list()
    for y in range(size):
        swapped_line = list()
        for x in range(size):
            swapped_line.append(swapped_dict[(x, y)])
        swapped.append(''.join(swapped_line))
    
    # Flip across the vertical axis to complete the rotation
    flipped = flip_pattern(line)
    
    # Return the pattern as a tuple of tuples so it can be hashed and used in a dictionary.
    return tuple(flip_pattern(swapped))


def flip_pattern(pattern):
    """ Flip the provided pattern horizontally (across the vertical axis) and returns it. """
    
    # Reverse each line to flip horizontally, and return as a tuple of tuples so it can be hashed.
    return tuple(line[::-1] for line in pattern)


def parse_rules(raw_enhancement_rules):
    """ Parse the enhancement rules and return a dictionary input patterns and the output patterns
    they produce.
    
    The rules are defined like this:
    
    .../.../... => .#.#/###./##.#/###.
    
    which indicate a 3x3 pattern which produces a 4x4 pattern:
    
    ...        .#.#
    ...  -->   ###.
    ...        ##.#
               ###.
    """

    rules_dict = dict()

    # For every rule in the input...
    for rule_line in raw_enhancement_rules:
        
        # Split the input from the output and turn the input/output into an iterable of lines
        input_side, output_side = rule_line.split(' => ')
        input_pattern = tuple(input_side.split('/'))
        output_pattern = tuple(output_side.split('/'))
        
        # Map the input to the output, and flip the input and map it again.
        rules_dict[input_pattern] = output_pattern
        rules_dict[flip_pattern(input_pattern)] = output_pattern
        
        # Then 3 times, both rotate and flip the input and map to the output, so we cover all
        # rotations and flips of the input pattern.
        for _ in range(3):
            input_pattern = rotate_pattern(input_pattern)
            rules_dict[input_pattern] = output_pattern
            rules_dict[flip_pattern(input_pattern)] = output_pattern

    return rules_dict
        

def _build_dict(pattern):
    """ Turn a pattern into a dictionary of coordinate to value at that coordinate. """
    
    pattern_dict = dict()
    for y, line in enumerate(pattern):
        for x, element in enumerate(line):
            pattern_dict[(x, y)] = element

    return pattern_dict


def enhance_chunks(chunks, rules):
    """ Given a set of chunks (smaller sub-patterns) and the enhancement rules from the input, turn
    each chunk into its enhanced version and return that new list. """

    return [rules[tuple(chunk)] for chunk in chunks]


def get_chunks(pattern, chunk_size, chunks_per_axis):
    """ Given the pattern, chunk size and number of chunks per axis, break the pattern into square
    chunks of the specified size and return a list of those chunks.
    
    Ex:  AAAA   -->   AA  AA   -->   [ AA,  AA,  DD,  EE
         BBCC         BB  CC           BB   CC   FF   FF ]
         DDEE
         FFFF         DD  EE
                      FF  FF
    """

    pattern_dict = _build_dict(pattern)
    
    # Get the coordinates of the top-left cell in each chunk
    chunk_corner_coords = list()
    for row_num in range(chunks_per_axis):
        y = row_num * chunk_size
        for col_num in range(chunks_per_axis):
            x = col_num * chunk_size
            chunk_corner_coords.append((x, y))

    # For each top-left corner of a chunk, build the chunk that's chunk_size large
    chunks = list()
    for corner_x, corner_y in chunk_corner_coords:
        chunk = list()
        
        # Each chunk is comprised of chunk_size rows
        for chunk_element_y in range(corner_y, corner_y+chunk_size):
            
            # Build each row, peeling of chunk_size length of the pattern at the correct coordinate
            chunk_row = list()
            for chunk_element_x in range(corner_x, corner_x+chunk_size):
                chunk_row.append(pattern_dict[(chunk_element_x, chunk_element_y)])
                
            # Append the row to the chunk
            chunk.append(''.join(chunk_row))
            
        # Append the completed chunk to the list of chunks
        chunks.append(chunk)
        
    return chunks


def reassemble_chunks(chunks, chunks_per_axis):
    """ Take a flat list of chunks and turn them back into a single grid (new pattern), given that
    the number of chunks per axis has remained the same (each chunk has just gotten bigger). """
    
    new_pattern = list()
    
    # While we still have more chunks to process in the list...
    while chunks:
        
        # Peel off chunks_per_axis chunks, which are the each row of the chunked pattern
        current_row_chunks, chunks = chunks[:chunks_per_axis], chunks[chunks_per_axis:]
        
        # Figure out the size of the chunks. This will correspond to how MANY rows this set
        # of chunks turns into.
        # Ex: a set of two 3x3 chunks makes up a single row of the chunked pattern, but will
        # turn into 3 rows of the new reassembled pattern.
        chunk_size = len(current_row_chunks[0])
        for i in range(chunk_size):
            
            # Start a new row of the reassembled pattern
            new_row = ''
            
            # Each row of the chunks are concatenated to make one row of the reassembled pattern.
            # Ex: 2 chunks that look like this:
            # AAA   DDD
            # BBB   EEE
            # CCC   FFF
            # Turn into 3 individual rows of the reassembled pattern which look like this:
            # AAADDD
            # BBBEEE
            # CCCFFF
            for chunk in current_row_chunks:
                new_row += chunk[i]
            
            # Append the new row to the reassembled pattern
            new_pattern.append(new_row)

    return new_pattern


def enhance_pattern(pattern, rules):
    """ Given a pattern, enhance it with the specified rules and return the pattern. """

    # Get the size of the pattern, the chunk size depending on if the pattern size is divisible by
    # 2 or 3, and finally the number of chunks on each side.
    # 
    # For an 8x8 pattern:
    # size = 8
    # chunk_size = 2
    # chunks_per_axis = 4
    # indicating that the 8x8 pattern gets broken in 4x4 = 16 chunks that are 2x2 in size
    size = len(pattern[0])
    chunk_size = 2 if size % 2 == 0 else 3
    chunks_per_axis = int(size / chunk_size)

    chunks = get_chunks(pattern, chunk_size, chunks_per_axis)
    enhanced_chunks = enhance_chunks(chunks, rules)

    return reassemble_chunks(enhanced_chunks, chunks_per_axis)


def _count_on_pixels(pattern):
    """ Return a count of "on" pixels (#) in the specified pattern. """
    count = 0
    for row in pattern:
        for c in row:
            if c == '#':
                count += 1
    return count

    
@aoc_output_formatter(2017, 21, 1, 'number of pixels on after 5 iterations', assert_answer=147)
def part_one(raw_enhancement_rules, pattern):
    rules = parse_rules(raw_enhancement_rules)

    for _ in range(5):
        pattern = enhance_pattern(pattern, rules)
        
    return _count_on_pixels(pattern)


@aoc_output_formatter(2017, 21, 2, 'number of pixels on after 18 iterations', assert_answer=1936582)
def part_two(raw_enhancement_rules, pattern):
    rules = parse_rules(raw_enhancement_rules)

    for _ in range(18):
        pattern = enhance_pattern(pattern, rules)
        
    return _count_on_pixels(pattern)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw_enhancement_rules = get_input(input_file)
    starting_pattern = ['.#.', '..#', '###']

    part_one(raw_enhancement_rules, starting_pattern)
    part_two(raw_enhancement_rules, starting_pattern)




    

# Simple placeholder lambda which does nothing
DO_NOTHING = lambda token: token

# ----------------------------------------------------------------------------------------------


def get_input(input_file):
    """Returns the input from the specified file path, as a list of raw lines from the input
    file with newlines removed."""

    return [x.replace("\n", "") for x in open(input_file).readlines()]


def get_input_grid_map(input_file):
    """Returns grid-based input from the specified file path, as a dictionary of (x, y)
    coordinates to the element at that coordinate."""

    raw_lines = get_input(input_file)

    input_map = dict()
    for y, line in enumerate(raw_lines):
        for x, element in enumerate(line):
            input_map[(x, y)] = element

    return input_map


def get_tokenized_input(input_file, split_str, transform=DO_NOTHING):
    """Returns the input for the specified AoC day, where each line is split by the supplied
    string and collected into a list of tokens, and the entire input is returned as a list of
    token lists. Optionally, the caller can supply a function to transform each token into a
    desired format.

    Ex.
    1,2,3           [['1', '2', '3'],
    4,5,6  ------>   ['4', '5', '6'],
    7,8,9            ['7', '8', '9']]"""

    tokenized = [line.split(split_str) for line in get_input(input_file)]
    transformed = [[transform(t) for t in line] for line in tokenized]

    return transformed


# Allows us to `eval` input lines which describe nested lists of integers and other lists
ACCEPTABLE_EVAL_CHARS = set("[],0123456789 ")


def safe_eval(raw_line):
    """Returns the `eval` of the provided line if it contains any content. Ensures the operation
    is safe before performing `eval` by ensuring the line only has acceptable characters, so
    we're not doing any os or sys calls, etc. Returns None if the line is empty."""

    if not raw_line:
        return None

    if not all(char in ACCEPTABLE_EVAL_CHARS for char in raw_line):
        raise ValueError(f'"{raw_line}" contains characters which are not allowed.')

    return eval(raw_line)

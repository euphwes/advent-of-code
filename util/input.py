# simple placeholder lambda which does nothing
DO_NOTHING = lambda token: token

#---------------------------------------------------------------------------------------------------

def get_input(input_file):
    """ Returns the input from the specified file path, as a list of raw lines from the input file
    with newlines removed. """

    return [x.replace('\n', '') for x in open(input_file).readlines()]


def get_tokenized_input(input_file, split_str, transform=DO_NOTHING):
    """ Returns the input for the specified AoC day, where each line is split by the supplied string
    and collected into a list of tokens, and the entire input is returned as a list of token lists.
    Optionally, the caller can supply a function to transform each token into a desired format.

    Ex.
    1,2,3           [['1', '2', '3'],
    4,5,6  ------>   ['4', '5', '6'],
    7,8,9            ['7', '8', '9']] """

    tokenized   = [line.split(split_str) for line in get_input(input_file)]
    transformed = [[transform(t) for t in line] for line in tokenized]

    return transformed

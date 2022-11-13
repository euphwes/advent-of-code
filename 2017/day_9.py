from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _clean_garbage(stream):
    """ Accept a stream, clean the garbage out of it, and return a tuple containing the cleaned
    stream itself, as well as a count of the number of garbage characters removed. """

    # While the stream contains ! (cancellations), remove the ! itself as well as the following
    # character which the ! cancels.
    try:
        while True:
            ix = stream.index('!')
            stream = stream[:ix] + stream[ix+2:]
    except ValueError:
        pass

    # What remains is garbage without any cancellations. Remove anything inside <> and count the
    # garbage characters removed (not including the framing <>).
    removed_garbage = 0
    try:
        while True:
            # Find the next < and the first > which follows it. `end_ix` the is index of the first
            # character after the >.
            ix = stream.index('<')
            end_ix = stream[ix:].index('>') + ix + 1

            # Trim the garbage and the framing <> out of the stream
            stream = stream[:ix] + stream[end_ix:]

            # The number of removed garbage characters is end_ix - ix - 2 because we're not counting
            # the two <> framing characters as garbage.
            removed_garbage += end_ix-ix-2
    except ValueError:
        pass

    return stream, removed_garbage


def _listify(stream):
    """ Accepts a cleaned stream and converts it into a Python list of nested inner lists, which
    makes it easier to navigate the stream later when scoring. """

    # Convert {} into [] so we can `eval` this into a list.
    stream = stream.replace('{', '[')
    stream = stream.replace('}', ']')

    # Sometimes the input contains leading extraneous commas like `[,[],[]]`, so strip these out
    # so it makes the string proper nested list Python syntax so we can `eval` it.
    stream = stream.replace('[,', '[')

    return eval(stream)


def _score_groups(stream, depth=0):
    """ Score the stream by scoring individual groups and returning the sum. The root group's score
    is 1, and each inner group's score is 1 + score of its parent group. """

    # This group's score is its own depth + 1
    score = depth + 1

    # If the group has children, add their scores to this group's score to get this group's
    # composite score.
    for inner_stream in stream:
        score += _score_groups(inner_stream, depth=depth+1)

    return score


@aoc_output_formatter(2017, 9, 1, 'score of groups in the stream')
def part_one(stream):
    clean_stream, _ = _clean_garbage(stream)
    return _score_groups(_listify(clean_stream))


@aoc_output_formatter(2017, 9, 2, 'number of garbage characters removed')
def part_two(stream):
    _, garbage_count = _clean_garbage(stream)
    return garbage_count

#---------------------------------------------------------------------------------------------------

def run(input_file):
    stream = get_input(input_file)[0]

    def _stream_copy():
        return ''.join(c for c in stream)

    part_one(_stream_copy())
    part_two(_stream_copy())

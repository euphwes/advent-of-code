""" Module providing utility functions related to iteration. """

def nested_iterable(iter1, iter2):
    """ A generator for yielding pairs of values built from iterator over two iterables in a nested
    for-loop fashion. """

    for a in iter1:
        for b in iter2:
            yield a, b


def int_stream(start=0, end=None):
    """ A generator yielding integers starting at `start` , continuing to (and including) `end`
    if a value is provided. """

    n = start
    while True:
        yield n
        if n == end:
            return
        n += 1

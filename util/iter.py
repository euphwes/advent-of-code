""" Module providing utility functions related to iteration. """

from typing import Collection, Iterable, Tuple


def repeat_forever(iter1):
    """A generator which yields values from a provided iterable indefinitely, starting back over
    once the iterator is exhausted."""

    while True:
        yield from iter1


def nested_iterable(iter1, iter2):
    """A generator for yielding pairs of values built from iterator over two iterables in a
    nested for-loop fashion."""

    for a in iter1:
        for b in iter2:
            yield a, b


def triple_iterable(iter1, iter2, iter3):
    """A generator for yielding triples of values built from iterator over three iterables in a
    nested for-loop fashion."""

    for a in iter1:
        for b in iter2:
            for c in iter3:
                yield a, b, c


def int_stream(start=0, end=None):
    """A generator yielding integers starting at `start`, continuing to (and including) `end`
    if a value is provided."""

    n = start
    while True:
        yield n
        if n == end:
            return
        n += 1


def bidirectional_range(start, end, inclusive=False):
    """Implements a bidirectional range, optionally inclusive of the end point.

    bidirectional_range(0, 3) = generator of (0, 1, 2)
    bidirectional_range(0, 3, inclusive=True) = generator of (0, 1, 2, 3)
    bidirectional_range(4, 1) = generator of (4, 3, 2)
    bidirectional_range(4, 1, inclusive=True) = generator of (4, 3, 2, 1)
    """

    # This is just a "regular" ascending range. We can yield from the built-in `range`.
    if start <= end:
        if inclusive:
            end += 1
        yield from range(start, end)

    # For the descending case, let's avoid using the built-in `range` and reversing it, because that
    # requires building the whole range in memory first so we can reverse it. Let's do it stepwise
    # and yield each value, so this is a proper generator.
    else:
        curr = start
        if inclusive:
            end -= 1
        while curr > end:
            yield curr
            curr -= 1


def min_and_max(values: Iterable[int]) -> Tuple[int, int]:
    """Returns a tuple of the min and max values in the provided iterable."""

    values = set(values)
    return min(values), max(values)

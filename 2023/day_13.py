from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 13
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of reflection summaries"
PART_ONE_ANSWER = 36015

PART_TWO_DESCRIPTION = "sum of reflection summaries after cleaning smudges"
PART_TWO_ANSWER = 35335


def _get_column(array, n):
    """For a given 2D array (a list of lists), return the values in the Nth column of that
    array as a list of those values."""

    return [row[n] for row in array]


def _does_reflect_horizontally(array, y):
    """Returns if the given array reflects at the horizontal line specified by the y-index."""

    top_half = array[:y]
    bottom_half = array[y:]

    # Only consider reflections valid if both partitions are not empty.
    if not top_half or not bottom_half:
        return False

    # Iterate of pairs of rows from each partition, starting from the bottom row of the
    # top partition, and the top row of the bottom partition. Unmatched rows will be ignored.
    # The array reflects at the y index if all row pairs match.
    return all(row1 == row2 for row1, row2 in zip(reversed(top_half), bottom_half))


def _does_reflect_vertically(array, x):
    """Returns if the given array reflects at the vertical line specified by the x-index."""

    # Partition the array into a left side and a right side at the provided x index.
    left_columns = []
    right_columns = []

    # Build the left partition going from the inside of the array towards the outside.
    # Stop when one side or the other reaches the left/right edge of the array.
    left_x = x - 1
    right_x = x
    while left_x >= 0 and right_x < len(array[0]):
        left_columns.append(_get_column(array, left_x))
        right_columns.append(_get_column(array, right_x))
        left_x -= 1
        right_x += 1

    # Only consider reflections valid if both arrays contain values.
    if not left_columns or not right_columns:
        return False

    # Iterate of pairs of columns from each partition. Unmatched columns will be ignored.
    # The array reflects at the x index if all column pairs match.
    return all(col1 == col2 for col1, col2 in zip(left_columns, right_columns))


def _extract_minimaps(raw_minimaps):
    """Parse a list of 2D arrays out of the problem input, where each array is separated by a
    line of whitespace."""

    minimaps = list()

    minimap = list()
    while raw_minimaps:
        line = raw_minimaps.pop(0)
        if line:
            minimap.append(line)
        else:
            minimaps.append(minimap)
            minimap = list()
    if minimap:
        minimaps.append(minimap)

    return minimaps


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_minimaps):
    minimaps = _extract_minimaps(raw_minimaps)

    rows_above_lines_of_reflection = 0
    cols_left_of_lines_of_reflection = 0

    for minimap in minimaps:
        for y in range(len(minimap)):
            if _does_reflect_horizontally(minimap, y):
                rows_above_lines_of_reflection += y
                break

    for minimap in minimaps:
        for x in range(len(minimap[0])):
            if _does_reflect_vertically(minimap, x):
                cols_left_of_lines_of_reflection += x
                break

    return cols_left_of_lines_of_reflection + (100 * rows_above_lines_of_reflection)


def _fix_smudge(minimap):
    """Fixes a 'smudge' in a map by altering a '#' to a '.', or vice versa, where such a
    correction results in a new, different line of reflection than the map originally had.

    Returns a representation of the new reflection, h/v[int], where h means the map
    has a horizontal reflection, and v means it reflects vertically, and the trailing integer
    is the index where the reflection occurs."""

    def _toggle(char):
        return "#.".replace(char, "")

    def _find_reflection(minimap, ignore_prev=None):
        for y in range(len(minimap)):
            if _does_reflect_horizontally(minimap, y):
                if ignore_prev is not None and ("h", y) == ignore_prev:
                    continue
                return ("h", y)

        for x in range(len(minimap[0])):
            if _does_reflect_vertically(minimap, x):
                if ignore_prev is not None and ("v", x) == ignore_prev:
                    continue
                return ("v", x)

        return None

    initial_reflection = _find_reflection(minimap)

    # Need to change the rows into lists because we need to alter a value at a particular index,
    # and strings are immutable.
    minimap = [list(line) for line in minimap]

    for y in range(len(minimap)):
        for x in range(len(minimap[0])):
            minimap[y][x] = _toggle(minimap[y][x])
            new_reflection = _find_reflection(minimap, ignore_prev=initial_reflection)
            if new_reflection is not None and new_reflection != initial_reflection:
                return new_reflection
            else:
                minimap[y][x] = _toggle(minimap[y][x])

    raise ValueError("unable to find a new reflection by fixing a smudge")


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_minimaps):
    minimaps = _extract_minimaps(raw_minimaps)
    reflecs = [_fix_smudge(minimap) for minimap in minimaps]

    rows_above_lines_of_reflection = sum(r[1] for r in reflecs if r[0] == "h")
    cols_left_of_lines_of_reflection = sum(r[1] for r in reflecs if r[0] == "v")

    return cols_left_of_lines_of_reflection + (100 * rows_above_lines_of_reflection)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    raw_minimaps = get_input(input_file)
    part_one(raw_minimaps)

    raw_minimaps = get_input(input_file)
    part_two(raw_minimaps)

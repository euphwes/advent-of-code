from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 18
YEAR = 2016

PART_ONE_DESCRIPTION = "safe tile count, small room"
PART_ONE_ANSWER = 1956

PART_TWO_DESCRIPTION = "safe tile count, big room"
PART_TWO_ANSWER = 19995121

PRIOR_STATES_FOR_CURR_TRAPS = {"^^.", ".^^", "^..", "..^"}


def _build_next_row(prior_row):
    """Builds and returns the next row of traps and safe tiles, which can be deterministically
    found from the previous row state."""

    # In the previous row, map index to the tile (. is safe, ^ is trap)
    prior_map = {i: prior_row[i] for i in range(len(prior_row))}

    # The left and rightmost tiles reference imaginary safe tiles outside the bounds of the row
    prior_map[-1] = "."
    prior_map[len(prior_row)] = "."

    # For each tile in the new row, its state is determined by the tile at the same position in
    # the previous row. If that prior state is one of the states in the set above, the new tile
    # is a trap, otherwise it's a safe tile.
    next_row = ""
    for i in range(len(prior_row)):
        prior_state = prior_map[i - 1] + prior_map[i] + prior_map[i + 1]
        next_row += "^" if prior_state in PRIOR_STATES_FOR_CURR_TRAPS else "."

    return next_row


def _get_room_safe_tile_count(row, total_rows):
    """Count the total number of safe tiles in the room, given a starting row and a total number
    of rows in the room."""

    safe_count = 0
    for _ in range(total_rows):
        safe_count += sum([1 for c in row if c == "."])
        row = _build_next_row(row)
    return safe_count


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(first_row):
    return _get_room_safe_tile_count(first_row, 40)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(first_row):
    return _get_room_safe_tile_count(first_row, 400000)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    first_row = get_input(input_file)[0]

    part_one(first_row)
    part_two(first_row)

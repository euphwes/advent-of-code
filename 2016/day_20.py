from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

DAY = 20
YEAR = 2016

PART_ONE_DESCRIPTION = "lowest value IP not blocked"
PART_ONE_ANSWER = 32259706

PART_TWO_DESCRIPTION = "how many IPs allowed by the blocklist"
PART_TWO_ANSWER = 113


def __normalize_blocklists(blocklist_ranges):
    """Normalize the blocklist ranges by combining overlapping ranges, and sorting them so that
    ranges with lower endpoints appear first."""

    # First sort by the end of the range, then the beginning of the range, so that lower starts
    # come first and for ranges with equal starts, the lower end comes first
    blocklist_ranges.sort(key=lambda x: x[1])
    blocklist_ranges.sort(key=lambda x: x[0])

    normalized_ranges = list()

    curr_range = None
    for blocklist_range in blocklist_ranges:
        if curr_range is None:
            curr_range = blocklist_range
            continue

        start, end = blocklist_range

        # If the new range starts at least 2 after the current ones ends, it's a new range.
        # Add the current range to the cleaned ranges and start tracking this new one.
        # Ex: [1, 5], [7, 8] are distinct ranges
        if start >= curr_range[1] + 2:
            normalized_ranges.append(curr_range)
            curr_range = blocklist_range

        # If the new range starts exactly where the current one ends, or 1 immediately after,
        # it's a continuation of the range because these ranges are inclusive on both sides.
        # Extend the current range.
        # Ex: [1, 5], [5, 9] --> [1, 9]
        # Ex: [1, 5], [6, 9] --> [1, 9]
        elif start in (curr_range[1], curr_range[1] + 1):
            curr_range[1] = end

        # If the new range starts inside the current one...
        elif start > curr_range[0] and start < curr_range[1]:
            # ... and it also ends inside the current one, nothing happens.
            # Ex: [1, 9], [3, 7] --> [1, 9]
            if end < curr_range[1]:
                pass

            # ... and it ends outside the current one, extend the current range to end where the
            # new one does.
            # Ex: [1, 5], [4, 9] --> [1, 9]
            else:
                curr_range[1] = end

    normalized_ranges.append(curr_range)
    return normalized_ranges


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(blocklist_ranges):
    # Normalize the blocklist ranges, and since we are confident the ranges are in order and
    # don't overlap, we can return the first number after the endpoint of the first blocklist
    # range.
    return __normalize_blocklists(blocklist_ranges)[0][1] + 1


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(blocklist_ranges):
    count = 0
    # For each pair of ranges, figure out how many values fall after the first range but before
    # the second range, and add that to the running count.
    blocklist_ranges = __normalize_blocklists(blocklist_ranges)
    for i in range(len(blocklist_ranges) - 1):
        range_a = blocklist_ranges[i]
        range_b = blocklist_ranges[i + 1]
        count += range_b[0] - range_a[1] - 1

    # The allowable IP range ends at 4294967295 (inclusive), so add the count of IPs which exist
    # after the end of last range.
    count += 4294967296 - range_b[1] - 1

    return count


# ----------------------------------------------------------------------------------------------


def run(input_file):
    blocklist_ranges = get_tokenized_input(input_file, "-", transform=int)

    part_one(blocklist_ranges[:])
    part_two(blocklist_ranges[:])

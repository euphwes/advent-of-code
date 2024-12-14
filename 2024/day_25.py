from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 25
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _parse_locks_keys(raw_input: list[str]) -> tuple[list[list[int]], list[list[int]]]:
    keys = []
    locks = []

    curr_key = [-1, -1, -1, -1, -1]
    curr_lock = [-1, -1, -1, -1, -1]
    known_type = None  # or "key" or "lock"

    while raw_input:
        line = raw_input.pop(0)
        if line == "":
            if known_type == "key":
                keys.append(curr_key)
            elif known_type == "lock":
                locks.append(curr_lock)
            else:
                raise ValueError("Unknown type")
            curr_key = [-1, -1, -1, -1, -1]
            curr_lock = [-1, -1, -1, -1, -1]
            known_type = None
            continue

        if known_type is None:
            if line == ".....":
                known_type = "key"
            elif line == "#####":
                known_type = "lock"
            else:
                raise ValueError("Unknown type")

        for i, char in enumerate(line):
            if char == ".":
                continue
            if known_type == "key":
                curr_key[i] += 1
            elif known_type == "lock":
                curr_lock[i] += 1
            else:
                raise ValueError("Unknown type")

    if known_type == "key":
        keys.append(curr_key)
    elif known_type == "lock":
        locks.append(curr_lock)
    else:
        raise ValueError("Unknown type")

    return keys, locks


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    keys, locks = _parse_locks_keys(raw_input)
    # print("\nkeys")
    # for k in keys:
    #     print(k)
    # print("\nlocks")
    # for l in locks:
    #     print(l)
    # return None

    valid_count = 0
    for k in keys:
        for l in locks:
            if all(k[i] + l[i] <= 5 for i in range(5)):
                valid_count += 1

    return valid_count


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    pass


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

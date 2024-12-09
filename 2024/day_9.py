from dataclasses import dataclass
from typing import Optional
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 9
YEAR = 2024

PART_ONE_DESCRIPTION = "filesystem checksum"
# PART_ONE_ANSWER = 6421128769094
# PART_ONE_ANSWER = 1928
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _is_ordered(memory):
    ix = memory.index(".")
    return all(c == "." for c in memory[ix:])


def _move_memory(memory):
    ix = memory.index(".")
    for jx in int_stream(1):
        if memory[-1 * jx] == ".":
            continue
        break
    memory[ix] = memory[-1 * jx]
    memory[-1 * jx] = "."
    return memory


def _checksum(memory):
    # print("".join(memory))
    return sum(i * int(n) for i, n in enumerate(memory) if n != ".")


def _checksum_v2(memory):
    other_rep = []
    for entry in memory:
        if entry[0] == "empty":
            other_rep.extend(entry[1] * ["."])
        else:
            other_rep.extend(entry[1] * [str(entry[2])])
    # print("")
    # print(other_rep)
    return _checksum(other_rep)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    memory = []

    curr_id = 0
    is_empty = False

    for char in stuff:
        ichar = int(char)
        if is_empty:
            memory.extend(ichar * ["."])
        else:
            memory.extend(ichar * [str(curr_id)])
            curr_id += 1
            pass
        is_empty = not is_empty

    # print(memory)
    while not _is_ordered(memory):
        memory = _move_memory(memory)
    # print(memory)
    return _checksum(memory)


def _get_file_ids_and_sizes(memory):
    file_ids_and_sizes = []
    for i, entry in enumerate(memory):
        if not entry[0] == "file":
            continue
        size, file_id = entry[1], entry[2]
        file_ids_and_sizes.append((file_id, size, i))

    # largest to smallest file_id
    file_ids_and_sizes.sort(key=lambda t: t[0], reverse=True)

    return file_ids_and_sizes


def _move_memory_v2(memory):

    file_ids_attempted = set()

    while True:
        file_ids_and_sizes = _get_file_ids_and_sizes(memory)

        for file_id, file_size, file_ix in file_ids_and_sizes:
            if file_id in file_ids_attempted:
                continue
            else:
                file_ids_attempted.add(file_id)
                break
        else:
            return memory

        empty_size = None
        empty_ix = None

        # chunks of free memory and indices
        for j, entry in enumerate(memory):
            if not entry[0] == "empty":
                continue
            empty_size = entry[1]
            if empty_size >= file_size:
                empty_ix = j
                break

        # nothing big enough to the left to hold this
        if empty_ix is None:
            continue

        # the empty space is later
        if empty_ix > file_ix:
            continue

        leftover_space = empty_size - file_size
        # print(
        #     f"\nswapping {file_id=} with {file_size=} with blanks at {empty_ix=} with {leftover_space=}"
        # )

        # put the file in the blank space
        memory[empty_ix] = ("file", file_size, file_id)

        # put the remaining leftover blank space after it, and the rest of the memory
        # after that
        if leftover_space:
            tmp_rest = memory[empty_ix + 1 :]
            memory = memory[: empty_ix + 1] + [("empty", leftover_space)] + tmp_rest

        # replace the moved file with empty space of the same size
        fix = None
        for ix, entry in enumerate(memory):
            if entry[0] == "file" and entry[2] == file_id:
                if fix is None:
                    fix = ix
                else:
                    fix = ix
                    break
        memory[fix] = ("empty", file_size)

        # if consecutive blocks of blank space, merge them
        while True:
            did_merge = False
            for ix, entry in enumerate(memory[:-1]):
                if entry[0] != "empty":
                    continue
                if memory[ix + 1][0] != "empty":
                    continue
                # both are blocks, merge them
                sizea, sizeb = entry[1], memory[ix + 1][1]
                memory[ix] = ("empty", sizea + sizeb)
                del memory[ix + 1]
                did_merge = True
                break

            if not did_merge:
                break

    return memory


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    memory = []

    curr_id = 0
    is_empty = False

    for char in stuff:
        ichar = int(char)
        if is_empty:
            memory.append(("empty", ichar))
        else:
            memory.append(("file", ichar, curr_id))
            curr_id += 1
        is_empty = not is_empty

    _checksum_v2(memory)
    memory = _move_memory_v2(memory)
    return _checksum_v2(memory)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff[0])

    stuff = get_input(input_file)
    # 87466167440 too low
    # 6676627190929 too high
    # 6698144357906 too high
    # 6449340599999, not right
    # 6449695642594, not right
    # 6448168620520
    part_two(stuff[0])

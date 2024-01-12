from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 15
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of HASH algorithm on each step of initialization seq"
PART_ONE_ANSWER = 509167

PART_TWO_DESCRIPTION = "focusing power of lens config"
PART_TWO_ANSWER = 259333


def _myhash(val):
    """Implement the hashing algorithm described in the problem input."""

    curr = 0
    for c in val:
        curr += ord(c)
        curr *= 17
        curr = curr % 256
    return curr


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(initialization_sequence):
    return sum(_myhash(s) for s in initialization_sequence[0].split(","))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(initialization_sequence):
    boxes = {x: [] for x in range(256)}

    instrs = initialization_sequence[0].split(",")
    for instr in instrs:
        if "-" in instr:
            label = instr.split("-")[0]
            boxnum = _myhash(label)

            lenses = boxes[boxnum]
            found_i = None
            for i, lens_label in enumerate(lenses):
                _, existing_label = lens_label
                if existing_label == label:
                    found_i = i
                    break

            if found_i is not None:
                lenses.pop(found_i)

        elif "=" in instr:
            label, focal_length = instr.split("=")
            boxnum = _myhash(label)

            lenses = boxes[boxnum]
            found_i = None
            for i, lens_label in enumerate(lenses):
                _, existing_label = lens_label
                if existing_label == label:
                    found_i = i
                    break

            if found_i is not None:
                lenses[i] = (focal_length, label)
            else:
                lenses.append((focal_length, label))

        else:
            raise ValueError(f"Unknown instruction: {instr}")

    score = 0
    for box in range(256):
        boxvalue = box + 1
        lenses = boxes[box]
        for i, lens_label in enumerate(lenses):
            focal_length, label = lens_label
            score += (boxvalue * (i + 1)) * int(focal_length)

    return score


# ----------------------------------------------------------------------------------------------


def run(input_file):
    initialization_sequence = get_input(input_file)
    part_one(initialization_sequence)

    initialization_sequence = get_input(input_file)
    part_two(initialization_sequence)

from copy import copy
from uuid import uuid4

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 20
YEAR = 2022

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _small_uuid():
    return str(uuid4())[:8]


def _translate_numbers(numbers):
    original_ordered_numbers = copy(numbers)

    ix_to_uuid = {i: _small_uuid() for i, _ in enumerate(numbers)}
    uuid_to_ix = {v: k for k, v in ix_to_uuid.items()}

    return (
        [ix_to_uuid[i] for i in range(len(numbers))],
        ix_to_uuid,
        uuid_to_ix,
        original_ordered_numbers,
    )


def _translate_uuids(numbers, original_ordered_values, uuid_to_original_ix):
    return [original_ordered_values[uuid_to_original_ix[uuid]] for uuid in numbers]


def _move_element_at_ix_by_value(elements, ix, value):
    if value == 0:
        return elements

    size = len(elements)
    target = (ix + value) % size

    if target == ix:
        if value > 0:
            elements[ix], elements[ix + 1] = elements[ix + 1], elements[ix]
        else:
            elements[ix], elements[ix - 1] = elements[ix - 1], elements[ix]
        return elements

    if value > 0:
        if target > ix:
            before = elements[:ix]
            after = elements[target + 1 :]
            middle = elements[ix : target + 1]

            temp = middle.pop(0)
            middle.append(temp)
            return before + middle + after
        else:
            before = elements[: target + 1]
            after = elements[ix + 1 :]
            middle = elements[target + 1 : ix + 1]

            temp = middle.pop(-1)
            middle = [temp] + middle
            return before + middle + after
    else:
        if target < ix:
            before = elements[:target]
            after = elements[ix + 1 :]
            middle = elements[target : ix + 1]

            temp = middle.pop(-1)
            middle = [temp] + middle
            return before + middle + after
        else:
            before = elements[:ix]
            after = elements[target:]
            middle = elements[ix:target]

            temp = middle.pop(0)
            middle.append(temp)
            return before + middle + after


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(numbers):

    # print(len(numbers))
    # return

    (
        translated_numbers,
        ix_to_uuid,
        uuid_to_ix,
        original_ordered_numbers,
    ) = _translate_numbers(numbers)

    # print("\nInitial")
    # print(original_ordered_numbers)

    for i in range(len(original_ordered_numbers)):
        original_value = original_ordered_numbers[i]
        target_uuid = ix_to_uuid[i]
        ix = translated_numbers.index(target_uuid)

        # if original_value == 5753:
        #     print(f"\nMove {original_value=} which is now at {ix=}")

        translated_numbers = _move_element_at_ix_by_value(
            translated_numbers,
            ix,
            original_value,
        )
        # print(
        #     _translate_uuids(translated_numbers, original_ordered_numbers, uuid_to_ix)
        # )

    numbers = _translate_uuids(translated_numbers, original_ordered_numbers, uuid_to_ix)

    i = numbers.index(0)
    size = len(numbers)

    return (
        numbers[(i + 1000) % size]
        + numbers[(i + 2000) % size]
        + numbers[(i + 3000) % size]
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    pass


# ----------------------------------------------------------------------------------------------


def run_tests():
    def _assert_equal(actual, expected):
        if expected != actual:
            raise AssertionError(f"Actual {actual} != expected {expected}")

    move = _move_element_at_ix_by_value

    # Move by 0 value doesn't change anything, for any ix.
    for ix in range(5):
        _assert_equal(
            move(list("ABCDE"), ix=ix, value=0),
            list("ABCDE"),
        )

    # Move by value that causes target and ix to be the same
    # TODO I'm not convinced this is right
    _assert_equal(
        move(list("abcde"), ix=2, value=5),
        list("abdce"),
    )
    _assert_equal(
        move(list("abcde"), ix=2, value=-5),
        list("acbde"),
    )

    # ####################
    # Positive value tests
    # ####################

    # Move positive value which is 1 less than the len of the sequence, doesn't change anything.
    # **** This should be equivalent to just doing nothing!! ****
    # ABCDE is equivalent to BCDEA if your consider it a circular list.
    # LOOK HERE if things are awry later.
    _assert_equal(
        move(list("abcde"), ix=0, value=4),
        list("bcdea"),
    )
    for ix in range(1, 5):
        _assert_equal(
            move(list("abcde"), ix=ix, value=4),
            list("abcde"),
        )

    # Move positive value to the right, not immediately adjacent, no wrapping, no edge touching.
    _assert_equal(
        move(list("abcdefgh"), ix=1, value=2),
        list("acdbefgh"),
    )
    _assert_equal(
        move(list("abcdefgh"), ix=1, value=5),
        list("acdefgbh"),
    )
    _assert_equal(
        move(list("abcdefgh"), ix=4, value=2),
        list("abcdfgeh"),
    )

    # Move positive value on left edge to the right, not reaching other edge
    _assert_equal(
        move(list("abcdefgh"), ix=0, value=2),
        list("bcadefgh"),  #
    )

    # Move positive value on left edge to the right, reaching other edge
    # **** This should be equivalent to just doing nothing!! ****
    # ABCDE is equivalent to BCDEA if your consider it a circular list.
    # LOOK HERE if things are awry later.
    _assert_equal(
        move(list("abcde"), ix=0, value=4),
        list("bcdea"),
    )

    # Move positive value to the right so far it wraps around and target is lower than ix.
    _assert_equal(
        move(list("abcdefgh"), ix=6, value=2),
        list("agbcdefh"),
    )
    _assert_equal(
        move(list("abcdefgh"), ix=5, value=4),
        list("abfcdegh"),
    )
    _assert_equal(
        move(list("abcde"), ix=4, value=2),
        list("abecd"),
    )
    _assert_equal(
        move(list("abcde"), ix=4, value=4),
        list("abcde"),
    )

    # ####################
    # Negative value tests
    # ####################

    # Move negative value to the left, not immediately adjacent, no wrapping, no edge touching.
    _assert_equal(
        move(list("abcdefgh"), ix=5, value=-2),
        list("abcfdegh"),
    )
    _assert_equal(
        move(list("abcdefgh"), ix=2, value=-1),
        list("acbdefgh"),
    )

    # Move negative value on right edge to the left, not reaching other edge
    _assert_equal(
        move(list("abcdefgh"), ix=7, value=-2),
        list("abcdehfg"),
    )

    # Move negative value on right edge to the left, reaching other edge
    # **** This should be equivalent to just doing nothing!! ****
    # ABCDE is equivalent to BCDEA if your consider it a circular list.
    # LOOK HERE if things are awry later.
    _assert_equal(
        move(list("abcde"), ix=4, value=-4),
        list("eabcd"),
    )

    # Move negative value to the left so far it wraps around and target is higher than ix.
    _assert_equal(
        move(list("abcdefgh"), ix=1, value=-3),
        list("acdefbgh"),
    )
    _assert_equal(
        move(list("abcdefgh"), ix=0, value=-5),
        list("bcadefgh"),
    )
    _assert_equal(
        move(list("abcdefgh"), ix=4, value=-5),
        list("abcdfgeh"),
    )

    # Move negative value which is 1 less than the len of the sequence, doesn't change anything.
    # **** This should be equivalent to just doing nothing!! ****
    # ABCDE is equivalent to BCDEA if your consider it a circular list.
    # LOOK HERE if things are awry later.
    _assert_equal(
        move(list("abcde"), ix=4, value=-4),
        list("eabcd"),
    )
    for ix in range(0, 4):
        _assert_equal(
            move(list("abcde"), ix=ix, value=-4),
            list("abcde"),
        )


# ----------------------------------------------------------------------------------------------


def run(input_file):

    run_tests()

    stuff = [int(n) for n in get_input(input_file)]
    part_one(stuff)

    # stuff = [int(n) for n in get_input(input_file)]
    # part_two(stuff)

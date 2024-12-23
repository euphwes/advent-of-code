from functools import cache
from itertools import permutations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 21
YEAR = 2024

PART_ONE_DESCRIPTION = "complexity of keycodes with 3 directional keypads"
PART_ONE_ANSWER = 157892

PART_TWO_DESCRIPTION = "complexity of keycodes with 26 directional keypads"
PART_TWO_ANSWER = 197015606336332


def _p(val):
    print(val)


NUMERIC_KEYPAD = [
    "789",
    "456",
    "123",
    " 0A",
]
NUMERIC_KEYPAD_COORDS = {
    char: (x, y) for y, row in enumerate(NUMERIC_KEYPAD) for x, char in enumerate(row)
}

DIRECTIONAL_KEYPAD = [
    " ^A",
    "<v>",
]
DIRECTIONAL_KEYPAD_COORDS = {
    char: (x, y) for y, row in enumerate(DIRECTIONAL_KEYPAD) for x, char in enumerate(row)
}


def _does_path_go_through_numeric_blank(scoord, path):
    sx, sy = scoord
    for char in path:
        if char == ">":
            sx += 1
        elif char == "<":
            sx -= 1
        elif char == "v":
            sy += 1
        elif char == "^":
            sy -= 1
        if NUMERIC_KEYPAD[sy][sx] == " ":
            return True
    return False


def _does_path_go_through_directional_blank(scoord, path):
    sx, sy = scoord
    for char in path:
        if char == ">":
            sx += 1
        elif char == "<":
            sx -= 1
        elif char == "v":
            sy += 1
        elif char == "^":
            sy -= 1
        if DIRECTIONAL_KEYPAD[sy][sx] == " ":
            return True
    return False


@cache
def _shortest_len_to_press_directional(
    path: str,
    num_directional_keypads_remaining: int = 3,
) -> int:
    # Let's say we're getting the path <^^A
    # From A to < we can go
    #     v<<, or <<v, or <v<, and then press A
    # From < to ^ we can go
    #     >^, or ^> ,and then press A
    # From ^ to ^ we don't need to go anywhere, just press A
    # From ^ to A we can go
    #     >, then press A
    # print()
    indent = "   " * (3 - num_directional_keypads_remaining)

    min_path_lengths = 0

    start_char = "A"
    for target_char in path:
        start_coord = DIRECTIONAL_KEYPAD_COORDS[start_char]
        target_coord = DIRECTIONAL_KEYPAD_COORDS[target_char]

        dx = target_coord[0] - start_coord[0]
        dy = target_coord[1] - start_coord[1]

        soln_base = ""
        if dx > 0:
            soln_base += ">" * dx
        elif dx < 0:
            soln_base += "<" * abs(dx)
        if dy > 0:
            soln_base += "v" * dy
        elif dy < 0:
            soln_base += "^" * abs(dy)

        if num_directional_keypads_remaining == 1:
            min_path_lengths += len(soln_base) + 1
            # _p(f"{indent+'   '}{start_char} to {target_char}, cost={len(soln_base) + 1}")
        else:
            min_path = min(
                _shortest_len_to_press_directional(
                    "".join(path) + "A",
                    num_directional_keypads_remaining - 1,
                )
                for path in permutations(soln_base)
                if not _does_path_go_through_directional_blank(start_coord, path)
            )
            # _p(f"{indent+'   '}{start_char} to {target_char}, cost={min_path}")
            min_path_lengths += min_path

        start_char = target_char

    # _p(
    #     f"{indent}path: {path}, num_keypads: {num_directional_keypads_remaining}, "
    #     f"best_cost: {min_path_lengths}",
    # )
    return min_path_lengths


@cache
def _shortest_len_to_press_numeric(
    start_char: str,
    target_char: str,
    num_directional_keypads: int = 3,
) -> int:
    start_coord = NUMERIC_KEYPAD_COORDS[start_char]
    target_coord = NUMERIC_KEYPAD_COORDS[target_char]

    dx = target_coord[0] - start_coord[0]
    dy = target_coord[1] - start_coord[1]

    soln_base = ""
    if dx > 0:
        soln_base += ">" * dx
    elif dx < 0:
        soln_base += "<" * abs(dx)
    if dy > 0:
        soln_base += "v" * dy
    elif dy < 0:
        soln_base += "^" * abs(dy)

    min_path = min(
        _shortest_len_to_press_directional("".join(path) + "A", num_directional_keypads)
        for path in permutations(soln_base)
        if not _does_path_go_through_numeric_blank(start_coord, path)
    )
    # _p(f"\n{start_char} to {target_char}, min_path: {min_path}")
    return min_path


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    complexity = 0

    for keycode in raw_input:
        # _p(f"\n===============\nLooking at keycode: {keycode}")
        num_of_final_keypad_presses = 0

        start_char = "A"
        for target_char in keycode:
            num_of_final_keypad_presses += _shortest_len_to_press_numeric(
                start_char,
                target_char,
                num_directional_keypads=2,
            )
            start_char = target_char

        complexity += num_of_final_keypad_presses * int(
            "".join(d for d in keycode if d.isdigit()),
        )
        # _p(
        #     f"Keycode: {keycode}, keypresses: {num_of_final_keypad_presses}, "
        #     f"value: {"".join(d for d in keycode if d.isdigit())}, complexity: {complexity}",
        # )

    return complexity


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    complexity = 0

    for keycode in raw_input:
        # _p(f"\n===============\nLooking at keycode: {keycode}")
        num_of_final_keypad_presses = 0

        start_char = "A"
        for target_char in keycode:
            num_of_final_keypad_presses += _shortest_len_to_press_numeric(
                start_char,
                target_char,
                num_directional_keypads=25,
            )
            start_char = target_char

        complexity += num_of_final_keypad_presses * int(
            "".join(d for d in keycode if d.isdigit()),
        )
        # _p(
        #     f"Keycode: {keycode}, keypresses: {num_of_final_keypad_presses}, "
        #     f"value: {"".join(d for d in keycode if d.isdigit())}, complexity: {complexity}",
        # )

    return complexity


def run(input_file: str) -> None:
    # 161468 too high
    part_one(get_input(input_file))
    part_two(get_input(input_file))
    print(_shortest_len_to_press_directional.cache_info())


assert """
==================
solving keycode: 508A

   5    0     8      A
<^^A  vvA  ^^^A  >vvvA

   <    ^  ^   A    v  v    A   ^  ^  ^   A   >   v  v  v    A
v<<A  >^A  A  >A  <vA  A  >^A  <A  A  A  >A  vA  <A  A  A  >^A
              10

  v   <  <     A   >    ^   A  A   >   A     <   v    A  A   >    ^   A     <     A  A  A   >   A    v    A     <     A  A  A   >    ^   A
<vA  <A  A  >>^A  vA  <^A  >A  A  vA  ^A  v<<A  >A  >^A  A  vA  <^A  >A  v<<A  >>^A  A  A  vA  ^A  <vA  >^A  v<<A  >>^A  A  A  vA  <^A  >A
                                      22
76*508


==================
solving keycode: 508A

   5    0     8      A
^^<A  vvA  ^^^A  >vvvA

 ^  ^    <     A    v  v    A   ^  ^  ^   A   >   v  v  v    A
<A  A  v<A  >>^A  <vA  A  >^A  <A  A  A  >A  vA  <A  A  A  >^A
              10

   <     A  A    v   <     A   >  >    ^   A     <   v    A  A   >    ^   A     <     A  A  A   >   A    v    A     <     A  A  A   >    ^   A
v<<A  >>^A  A  <vA  <A  >>^A  vA  A  <^A  >A  v<<A  >A  >^A  A  vA  <^A  >A  v<<A  >>^A  A  A  vA  ^A  <vA  >^A  v<<A  >>^A  A  A  vA  <^A  >A
                                          26
"""  # noqa: PLW0129, S101

from collections import defaultdict
from heapq import heappop, heappush

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 21
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

NUMERIC_KEYPAD_GRAPH = {
    "A": {
        ("0", "<"),
        ("3", "^"),
    },
    "0": {
        ("A", ">"),
        ("2", "^"),
    },
    "1": {
        ("4", "^"),
        ("2", ">"),
    },
    "2": {
        ("1", "<"),
        ("0", "v"),
        ("3", ">"),
        ("5", "^"),
    },
    "3": {
        ("A", "v"),
        ("2", "<"),
        ("6", "^"),
    },
    "4": {
        ("1", "v"),
        ("5", ">"),
        ("7", "^"),
    },
    "5": {
        ("2", "v"),
        ("6", ">"),
        ("8", "^"),
        ("4", "<"),
    },
    "6": {
        ("3", "v"),
        ("5", "<"),
        ("9", "^"),
    },
    "7": {
        ("4", "v"),
        ("8", ">"),
    },
    "8": {
        ("5", "v"),
        ("7", "<"),
        ("9", ">"),
    },
    "9": {
        ("6", "v"),
        ("8", "<"),
    },
}

DIRECTIONAL_KEYPAD_GRAPH = {
    "A": {
        ("^", "<"),
        (">", "v"),
    },
    "^": {
        ("A", ">"),
        ("v", "v"),
    },
    "<": {
        ("v", ">"),
    },
    "v": {
        ("<", "<"),
        (">", ">"),
        ("^", "^"),
    },
    ">": {
        ("A", "^"),
        ("v", "<"),
    },
}


def _get_keypad_direction_chart(keypad):
    directions = defaultdict(dict)

    for start_key in keypad:
        for end_key in keypad:
            if start_key == end_key:
                directions[start_key][end_key] = ""
                continue

            visited = set()

            # queue is a list of (distance, num_dir_changes, key, path)
            queue = []
            heappush(queue, (0, start_key, ""))

            while queue:
                distance, key, path = heappop(queue)
                if key in visited:
                    continue
                visited.add(key)

                if key == end_key:
                    # >>> sorted('^><v')
                    # ['<', '>', '^', 'v']
                    min_dir_changes_path = "".join(sorted(path))

                    # if we're in the 1,4,7 column, we need to go right before going down
                    if start_key in "147" and end_key in "0A":
                        # print(
                        #     f"\nstart: {start_key}, end: {end_key}, path: {min_dir_changes_path}",
                        # )
                        pass
                        # shouldn't need to change anything

                    # if we're in 0,A and going to 1,4,7, need to go up before going left
                    elif start_key in "0A" and end_key in "147":
                        # print(
                        #     f"\nstart: {start_key}, end: {end_key}, path: {min_dir_changes_path}",
                        # )
                        # reverse path
                        min_dir_changes_path = min_dir_changes_path[::-1]
                        # print(
                        #     f"\nstart: {start_key}, end: {end_key}, path: {min_dir_changes_path}",
                        # )

                    elif start_key in "^A" and end_key == "<":
                        # need to go down before going left
                        min_dir_changes_path = min_dir_changes_path[::-1]

                    elif start_key == "<" and end_key in "^A":
                        # need to go right before going up
                        pass

                    if start_key == "A" and end_key == "5":
                        # TEST CASE
                        # reverse this even though it doesn't need it
                        min_dir_changes_path = min_dir_changes_path[::-1]

                    directions[start_key][end_key] = min_dir_changes_path
                    break

                for neighbor_key, neighbor_direction in keypad[key]:
                    if neighbor_key not in visited:
                        new_path = path + neighbor_direction
                        heappush(
                            queue,
                            (
                                distance + 1,
                                neighbor_key,
                                new_path,
                            ),
                        )

    return directions


def _p(val):
    print(val)


def _debug_paths(target_path, new_path):
    target_path = list(target_path)

    target_to_print = ""
    new_to_print = ""

    for chunk in new_path.split("A")[:-1]:
        new_to_print += chunk + "A  "
        target_to_print += (" " * len(chunk)) + target_path.pop(0) + "  "

    print(f"\n{target_to_print}\n{new_to_print}")


def _solve_keycode(keycode, numeric_keypad_paths, directional_keypad_paths):
    _p(f"\n==================\nsolving keycode: {keycode}")
    path = ""
    curr_char = "A"

    for char in keycode:
        path += numeric_keypad_paths[curr_char][char]
        path += "A"
        curr_char = char

    paths = []
    paths.append(path)
    _debug_paths(keycode, path)

    for _ in range(2):
        target_path = paths[-1]
        curr_char = "A"
        next_path = ""

        for char in target_path:
            next_path += directional_keypad_paths[curr_char][char]
            next_path += "A"
            curr_char = char

        paths.append(next_path)
        _debug_paths(target_path, next_path)

    length = len(paths[-1])
    keycode_digits = int("".join(c for c in keycode if c.isdigit()))
    print(f"\n{length}*{keycode_digits}")
    return length * keycode_digits


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    numeric_keypad_paths = _get_keypad_direction_chart(NUMERIC_KEYPAD_GRAPH)
    directional_keypad_paths = _get_keypad_direction_chart(DIRECTIONAL_KEYPAD_GRAPH)

    print("==============")
    return sum(
        _solve_keycode(keycode, numeric_keypad_paths, directional_keypad_paths)
        for keycode in raw_input
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    pass


def run(input_file: str) -> None:
    # 161468 too high
    part_one(get_input(input_file))
    part_two(get_input(input_file))

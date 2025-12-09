from collections import defaultdict
from collections.abc import Callable
from functools import cache
from itertools import combinations

from PIL import Image

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 9
YEAR = 2025

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

Coord = tuple[int, int]
Range = tuple[Coord, Coord]


def _parse(lines):
    foo = []
    for line in lines:
        a, b = line.split(",")
        foo.append((int(a), int(b)))
    return foo


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    coords = _parse(raw_input)

    m = -1
    for c1, c2 in combinations(coords, 2):
        x1, y1 = c1
        x2, y2 = c2

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        m = max((dx + 1) * (dy + 1), m)

    return m


def _get_is_in_shape_fn(perimeter_ranges: list[Range]) -> Callable[[Coord], bool]:
    """Get a thing."""

    # Remember corners to facilitate deciding if we're entering or exiting.
    corners_dict: dict[Coord, str] = {}
    for i in range(len(perimeter_ranges)):
        range1 = perimeter_ranges[i]
        range2 = perimeter_ranges[(i + 1) % len(perimeter_ranges)]

        other1, corner = range1
        _, other2 = range2

        cx, cy = corner

        rels = set()
        for other in [other1, other2]:
            ox, oy = other
            if ox < cx and oy == cy:
                rels.add("L")
            elif ox > cx and oy == cy:
                rels.add("R")
            elif oy > cy:
                rels.add("D")
            else:
                rels.add("U")

        if rels == set("UL"):
            corners_dict[corner] = "J"
        elif rels == set("UR"):
            corners_dict[corner] = "L"
        elif rels == set("DL"):
            corners_dict[corner] = "7"
        else:
            corners_dict[corner] = "F"

    # Store full set of coords of perimeter
    perimeter: set[Coord] = set()
    for r in perimeter_ranges:
        for c in _iter_coords(r[0], r[1]):
            perimeter.add(c)

    # Perimeter coords by y (each line)
    perim_by_y: dict[int, list[int]] = defaultdict(list)
    for cx, cy in perimeter:
        perim_by_y[cy].append(cx)

    perim_by_y = dict(perim_by_y)
    for v in perim_by_y.values():
        v.sort()

    # Dump image
    if False:
        # Create a smaller image
        img = Image.new("RGB", (2000, 2000), "white")
        pixels = img.load()
        assert pixels

        # Downscale and thicken
        for coord in perimeter:
            # Scale down the coordinate
            scaled_x = coord[0] // 50
            scaled_y = coord[1] // 50

            # Draw a 3x3 super-pixel centered on the scaled coordinate
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x = scaled_x + dx
                    y = scaled_y + dy
                    # Check bounds
                    if 0 <= x < 2000 and 0 <= y < 2000:
                        pixels[x, y] = (0, 0, 0)

        img.save("day_9.png")

    FLIP_PAIRS = set([frozenset("L7"), frozenset("FJ")])

    @cache
    def _is_in_shape(target: Coord) -> bool:
        """Do a thing."""

        if target in perimeter:
            return True

        # Otherwise we need to scan left to right and every time we cross
        # a vertical range we know we toggle between outside and inside the shape.
        # Keep doing that until we reach our target coordinate.

        tx, ty = target

        toggle_after_x_on_this_y: list[tuple[int, bool]] = []

        corner_buffer = []

        for x in perim_by_y[ty]:
            if (x, ty) in corners_dict:
                char = corners_dict[(x, ty)]
                if not corner_buffer:
                    corner_buffer.append(char)
                else:
                    other_char = corner_buffer.pop()
                    pair = frozenset(f"{char}{other_char}")
                    if pair in FLIP_PAIRS:
                        toggle_after_x_on_this_y.append((x, True))
                    else:
                        toggle_after_x_on_this_y.append((x, False))
            elif not corner_buffer:
                toggle_after_x_on_this_y.append((x, True))

        is_inside = False
        for px, should_toggle in toggle_after_x_on_this_y:
            if tx < px:
                return is_inside
            if should_toggle:
                is_inside = not is_inside

        err_msg = f"Shouldn't get here. {target}"
        raise ValueError(err_msg)

    return _is_in_shape


def _iter_coords(c1, c2):
    x1, y1 = c1
    x2, y2 = c2

    x1, x2 = tuple(sorted((x1, x2)))
    y1, y2 = tuple(sorted((y1, y2)))

    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            yield (x, y)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    coords: list[Coord] = _parse(raw_input)

    perimeter_ranges: list[Range] = []
    for i in range(len(coords)):
        c1, c2 = coords[i], coords[(i + 1) % len(coords)]
        perimeter_ranges.append((c1, c2))

    is_in_shape = _get_is_in_shape_fn(perimeter_ranges)

    # tests = [
    #     ((7, 1), True),
    #     ((8, 1), True),
    #     ((12, 1), False),
    #     ((11, 1), True),
    #     ((11, 5), True),
    #     ((11, 8), False),
    # ]

    # for t, expected in tests:
    #     calculated = is_in_shape(t)
    #     mark = "" if calculated == expected else "  *****"
    #     print(f"{t}: {expected=}, {calculated=}{mark}")

    possible_rects_size_first = []

    m = -1
    for c1, c2 in combinations(coords, 2):
        x1, y1 = c1
        x2, y2 = c2

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # if the rect defined by these two corners is bigger than the
        # previous max, then we check if it's entirely contained in the
        # enclosed area, to save on runtime

        new_size = (dx + 1) * (dy + 1)

        possible_rects_size_first.append((new_size, c1, c2))
        continue

    possible_rects_size_first.sort(key=lambda t: t[0], reverse=True)

    for new_size, c1, c2 in possible_rects_size_first:
        # if every spot on the perimeter of the proposed rectangle is inside
        # the larger shape, it's valid.

        #   c1 ---> c3
        #   c4 <--- c2

        c3 = (x1, y2)
        c4 = (x2, y1)

        is_invalid = False

        for corner in (c3, c4):
            if not is_in_shape(corner):
                is_invalid = True
                break

        if is_invalid:
            continue

        for nc in _iter_coords(c1, c3):
            if not is_in_shape(nc):
                is_invalid = True
                break

        if is_invalid:
            continue

        for nc in _iter_coords(c3, c2):
            if not is_in_shape(nc):
                is_invalid = True
                break

        if is_invalid:
            continue

        for nc in _iter_coords(c2, c4):
            if not is_in_shape(nc):
                is_invalid = True
                break

        if is_invalid:
            continue

        for nc in _iter_coords(c4, c1):
            if not is_in_shape(nc):
                is_invalid = True
                break

        if is_invalid:
            continue

        # yay, valid
        return new_size

    err = "shouldn't get here"
    raise ValueError(err)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

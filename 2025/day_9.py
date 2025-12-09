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

    # Remember min x and max x so we can do a horizontal scan later.
    all_xs: set[int] = set()
    all_ys: set[int] = set()
    for c1, c2 in perimeter_ranges:
        x1, y1 = c1
        x2, y2 = c2
        all_xs.add(x1)
        all_xs.add(x2)
        all_ys.add(y1)
        all_ys.add(y2)

    # Remember 1 before and after 1 min/max so we start outside when doing a scan.
    min_x = min(all_xs) - 2
    max_x = max(all_xs) + 2

    min_y = min(all_ys) - 2
    max_y = max(all_ys) + 2

    # Separate vertical and horizontal ranges for easier writing of logic later.
    vertical_ranges: list[Range] = []
    horizontal_ranges: list[Range] = []

    for c1, c2 in perimeter_ranges:
        if c1[1] == c2[1]:
            horizontal_ranges.append((c1, c2))
        else:
            vertical_ranges.append((c1, c2))

    @cache
    def _is_in_vertical_range(target: Coord) -> bool:
        """Do a thing."""

        tx, ty = target

        for c1, c2 in vertical_ranges:
            x1, y1 = c1
            _, y2 = c2

            if tx == x1 and min((y1, y2)) <= ty <= max((y1, y2)):
                return True

        return False

    @cache
    def _is_in_horizontal_range(target: Coord) -> bool:
        """Do a thing."""

        tx, ty = target

        for c1, c2 in horizontal_ranges:
            x1, y1 = c1
            x2, _ = c2

            if ty == y1 and min((x1, x2)) <= tx <= max((x1, x2)):
                return True

        return False

    # ======== DEBUG ==========

    def _p(demo_coord):
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                asd = (x, y)
                char = " "
                if asd == demo_coord:
                    char = "X"
                elif asd in corners_dict:
                    char = corners_dict[asd]
                elif _is_in_horizontal_range(asd) or _is_in_vertical_range(asd):
                    char = "#"
                print(f"{char}", end="")
            print()

    if False:
        _p(None)

    # ======== DEBUG ==========

    FLIP_PAIRS = set([frozenset("L7"), frozenset("FJ")])

    @cache
    def _is_in_shape(target: Coord) -> bool:
        """Do a thing."""

        if target in corners_dict:
            return True

        # A coord is in the shape if it's directly in any of the ranges
        if _is_in_horizontal_range(target):
            return True

        if _is_in_vertical_range(target):
            return True

        # Otherwise we need to scan left to right and every time we cross
        # a vertical range we know we toggle between outside and inside the shape.
        # Keep doing that until we reach our target coordinate.

        tx, ty = target

        is_inside = False
        corners: list[str] = []

        for test_x in range(min_x, max_x):
            test_coord = (test_x, ty)

            if test_x == tx:
                # if not is_inside:
                #     _p(test_coord)
                return is_inside

            # Crossing a vertical range means we potentially toggle
            if _is_in_vertical_range(test_coord):
                # If we're on a horizontal range too, we need to check the
                # corners of the attached vertical ranges to see if we toggle
                # in/out or not.
                if _is_in_horizontal_range(test_coord):
                    if test_coord in corners_dict:
                        if not corners:
                            corners.append(corners_dict[test_coord])
                        else:
                            char = corners_dict[test_coord]
                            other_char = corners.pop()
                            pair = frozenset(f"{char}{other_char}")
                            if pair in FLIP_PAIRS:
                                is_inside = not is_inside

                # If we're not also on a horizontal range, we can just cleanly toggle
                else:
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

    # Store full set of coords of perimeter
    perimeter: set[Coord] = set()
    for r in perimeter_ranges:
        for c in _iter_coords(r[0], r[1]):
            perimeter.add(c)

    # Dump image
    if True:
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
        return None

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

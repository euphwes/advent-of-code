from collections import defaultdict
from collections.abc import Callable, Generator
from functools import cache
from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 9
YEAR = 2025

PART_ONE_DESCRIPTION = "area of largest rectangle on red corners"
PART_ONE_ANSWER = 4739623064

PART_TWO_DESCRIPTION = "area of largest rectangle of only red and green tiles"
PART_TWO_ANSWER = 1654141440


Coord = tuple[int, int]
Range = tuple[Coord, Coord]


def _parse_coords(lines: list[str]) -> list[Coord]:
    ranges: list[Coord] = []
    for line in lines:
        a, b = tuple(int(n) for n in line.split(","))
        ranges.append((int(a), int(b)))

    return ranges


def _area_of_rect_defined_by(c1: Coord, c2: Coord) -> int:
    """Return the area of a rectangle with opposite corners at c1, c2."""

    x1, y1 = c1
    x2, y2 = c2

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    return (dx + 1) * (dy + 1)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    coords = _parse_coords(raw_input)
    possible_rects_sizes = [
        _area_of_rect_defined_by(c1, c2) for c1, c2 in combinations(coords, 2)
    ]

    return max(possible_rects_sizes)


def _get_is_in_shape_fn(ranges: list[Range]) -> Callable[[Coord], bool]:
    """Return a function returns if a coordinate is inside the shape defined by `ranges`."""

    # Remember corners to facilitate deciding if we're entering or exiting.
    corners_dict: dict[Coord, str] = {}
    for i in range(len(ranges)):
        range1 = ranges[i]
        range2 = ranges[(i + 1) % len(ranges)]

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
    for r in ranges:
        for c in _iter_coords(r[0], r[1]):
            perimeter.add(c)

    # Perimeter coords by y (each line)
    perim_by_y: dict[int, list[int]] = defaultdict(list)
    for cx, cy in perimeter:
        perim_by_y[cy].append(cx)

    perim_by_y = dict(perim_by_y)
    for v in perim_by_y.values():
        v.sort()

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
                    if pair in {frozenset("L7"), frozenset("FJ")}:
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

        return False

    return _is_in_shape


def _iter_coords(c1: Coord, c2: Coord) -> Generator[Coord]:
    """Iterate over coordinates between c1 (inclusive) and c2 (exclusive)."""

    x1, y1 = c1
    x2, y2 = c2

    x1, x2 = tuple(sorted((x1, x2)))
    y1, y2 = tuple(sorted((y1, y2)))

    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            yield (x, y)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    coords: list[Coord] = _parse_coords(raw_input)

    perimeter_ranges: list[Range] = []
    for i in range(len(coords)):
        c1, c2 = coords[i], coords[(i + 1) % len(coords)]
        perimeter_ranges.append((c1, c2))

    is_in_shape = _get_is_in_shape_fn(perimeter_ranges)

    possible_rects_size_first = []

    # From plotting and visually inspecting the shape defined by the input,
    # you can see the largest coordinate must be "anchored" with one corner
    # at the very end of the long vertical line inside the rough circle.
    # If the anchor point is on top, the other point of the rectangle must be on top.
    # Vice versa for the bottom.
    #
    # (94693, 48547) in the top half
    # (94693, 50233) in the bottom half

    top_half_coords = {(cx, cy) for cx, cy in coords if cy <= 50_000}
    bottom_half_coords = {(cx, cy) for cx, cy in coords if cy > 50_000}

    # TODO: I'm iterating over ALL 2nd points in each half of the circle, but we
    # can limit this to only check the points where the delta Y wouldn't cause
    # an edge of the rectangle to go outside the circle.

    # Construct all possible rectangles with corners anchored on the two anchor points.
    c1 = (94693, 48547)
    for c2 in top_half_coords:
        x1, y1 = c1
        x2, y2 = c2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        new_size = (dx + 1) * (dy + 1)
        possible_rects_size_first.append((new_size, c1, c2))

    c1 = (94693, 50233)
    for c2 in bottom_half_coords:
        x1, y1 = c1
        x2, y2 = c2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        new_size = (dx + 1) * (dy + 1)
        possible_rects_size_first.append((new_size, c1, c2))

    # Sort them by descending area, so we can check if they are entirely inside the shape
    # and the first one which is, we know is the largest possible area.
    possible_rects_size_first.sort(key=lambda t: t[0], reverse=True)

    for size, c1, c2 in possible_rects_size_first:
        x1, y1 = c1
        x2, y2 = c2

        # The other two corners of the rectangle, defined by opposite corners c1, c2
        c3 = (x1, y2)
        c4 = (x2, y1)

        is_invalid = False

        for rect_perimeter_coord in (
            rect_perimeter_coord
            for rect_side in (
                _iter_coords(c1, c3),
                _iter_coords(c3, c2),
                _iter_coords(c2, c4),
                _iter_coords(c4, c1),
            )
            for rect_perimeter_coord in rect_side
        ):
            if not is_in_shape(rect_perimeter_coord):
                is_invalid = True
                break

        # If any point on the perimeter of the rectangle is not inside the shape,
        # we know the rectangle is invalid and can skip to the next one.
        if is_invalid:
            continue

        return size

    raise ValueError("shouldn't be possible to get here")


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

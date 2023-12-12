from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 13
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = 36015

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = 35335


def _do_rows_reflect(t1, t2):
    if not t1 or not t2:
        return False

    for f1, f2 in zip(reversed(t1), t2):
        if f1 != f2:
            return False

    return True


def _do_cols_reflect(minimap, xx):
    first_cols = []
    second_cols = []

    # if xx == 0:
    #     return False

    try:
        x1 = xx - 1
        x2 = xx
        while x1 >= 0:
            col1 = []
            col2 = []
            for row in minimap:
                n1 = row[x1]
                n2 = row[x2]
                col1.append(n1)
                col2.append(n2)

            first_cols.append(col1)
            second_cols.append(col2)
            x1 -= 1
            x2 += 1
    except IndexError:
        pass

    # from pprint import pprint

    # print("first_cols")
    # pprint(first_cols)

    # print("second_cols")
    # pprint(second_cols)

    if not first_cols or not second_cols:
        return False, 0

    for c1, c2 in zip(first_cols, second_cols):
        if c1 != c2:
            # print("no match")
            # print(c1)
            # print(c2)
            return False, 0

    return True, xx


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    cols_left_of_lines_of_reflection = 0
    rows_above_lines_of_reflection = 0

    minimaps = list()

    minimap = list()
    while stuff:
        line = stuff.pop(0)
        if line:
            minimap.append(line)
        else:
            minimaps.append(minimap)
            minimap = list()
    if minimap:
        minimaps.append(minimap)

    horizs = set()
    verts = set()

    for i, minimap in enumerate(minimaps):
        for y in range(len(minimap)):
            above = minimap[:y]
            below = minimap[y:]
            if _do_rows_reflect(above, below):
                # print(f"minimap {i=} reflected horizontally at {y=}")
                horizs.add(i)
                rows_above_lines_of_reflection += len(above)
                break

    # from pprint import pprint

    # pprint(minimaps[0])
    # print()
    # pprint(minimaps[1])

    for i, minimap in enumerate(minimaps):
        for x in range(len(minimap[0])):
            # print(f"\ntrying {x=}")
            didpass, ncols = _do_cols_reflect(minimap, x)
            if didpass:
                # print(f"minimap {i=} reflected vertically at {x=}")
                cols_left_of_lines_of_reflection += ncols
                verts.add(i)
                break

    # both = verts.intersection(horizs)
    # if both:
    #     print(f"maps in both = {both}")

    # allmaps = horizs.union(verts)
    # print(f"{len(allmaps)=}")
    # print(f"{len(minimaps)=}")

    # missing_maps = set(range(100)) - allmaps
    # print(f"missing maps = {missing_maps}")

    return cols_left_of_lines_of_reflection + (100 * rows_above_lines_of_reflection)


def _toggle(charr):
    if charr == ".":
        return "#"
    elif charr == "#":
        return "."
    raise ValueError()


def _fix_smudge(i, orig_minimap):
    initial_reflection = None

    def test_a_map(minimap, ignore_prev=None):
        for y in range(len(minimap)):
            above = minimap[:y]
            below = minimap[y:]
            if _do_rows_reflect(above, below):
                if ignore_prev is not None and f"h{y}" == ignore_prev:
                    continue
                return f"h{y}"

        for x in range(len(minimap[0])):
            didpass, ncols = _do_cols_reflect(minimap, x)
            if didpass:
                if ignore_prev is not None and f"v{x}" == ignore_prev:
                    continue
                return f"v{x}"

        return None

    initial_reflection = test_a_map(orig_minimap)

    test_minimap = [list(line) for line in orig_minimap]

    for y in range(len(test_minimap)):
        for x in range(len(test_minimap[0])):
            test_minimap[y][x] = _toggle(test_minimap[y][x])
            new_reflection = test_a_map(test_minimap, ignore_prev=initial_reflection)
            # print(f"new -> {new_reflection}")
            if new_reflection is not None and new_reflection != initial_reflection:
                print(
                    f"fixed smudge for minimap {i}, {initial_reflection} --> {new_reflection}"
                )
                return test_minimap, new_reflection
            else:
                test_minimap[y][x] = _toggle(test_minimap[y][x])

    print(f"could not fix for {i=}, orig was {initial_reflection}")
    raise ValueError()


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    cols_left_of_lines_of_reflection = 0
    rows_above_lines_of_reflection = 0

    minimaps = list()

    minimap = list()
    while stuff:
        line = stuff.pop(0)
        if line:
            minimap.append(line)
        else:
            minimaps.append(minimap)
            minimap = list()
    if minimap:
        minimaps.append(minimap)

    minimaps = [_fix_smudge(i, minimap) for i, minimap in enumerate(minimaps)]
    reflecs = [x[1] for x in minimaps]
    minimaps = [x[0] for x in minimaps]

    # for reflect in minimaps:
    #     d = reflect[0]
    #     c = int(reflect[1:])
    #     if d == "h":
    #         cols_left_of_lines_of_reflection += c + 1
    #     elif d == "v":
    #         rows_above_lines_of_reflection += c

    horizs = set()
    verts = set()

    for i, minimap in enumerate(minimaps):
        for y in range(len(minimap)):
            above = minimap[:y]
            below = minimap[y:]
            if _do_rows_reflect(above, below):
                # print(f"minimap {i=} reflected horizontally at {y=}")
                horizs.add(i)
                if f"h{y}" == reflecs[i]:
                    rows_above_lines_of_reflection += len(above)
                    break

    # from pprint import pprint

    # pprint(minimaps[0])
    # print()
    # pprint(minimaps[1])

    for i, minimap in enumerate(minimaps):
        for x in range(len(minimap[0])):
            # print(f"\ntrying {x=}")
            didpass, ncols = _do_cols_reflect(minimap, x)
            if didpass:
                # print(f"minimap {i=} reflected vertically at {x=}")
                if f"v{x}" == reflecs[i]:
                    cols_left_of_lines_of_reflection += ncols
                    verts.add(i)
                    break

    both = verts.intersection(horizs)
    if both:
        print(f"maps in both = {both}")

    allmaps = horizs.union(verts)
    print(f"{len(allmaps)=}")
    print(f"{len(minimaps)=}")

    missing_maps = set(range(100)) - allmaps
    print(f"missing maps = {missing_maps}")

    return cols_left_of_lines_of_reflection + (100 * rows_above_lines_of_reflection)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)

    part_one(stuff)

    stuff = get_input(input_file)

    # not 40902
    # not 33850, too low
    # 33799 ? too low
    # 33901 ? no, but no high/low
    # 35335 ?
    part_two(stuff)

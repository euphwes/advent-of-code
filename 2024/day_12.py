from util.decorators import aoc_output_formatter
from util.input import get_input
from util.structures import get_neighbors_of

from itertools import combinations

DAY = 12
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _neighbors(coord, grid):
    height = grid[coord]
    neighbors = list()

    cx, cy = coord
    for neighbor_coord in [(cx, cy + 1), (cx, cy - 1), (cx + 1, cy), (cx - 1, cy)]:
        if neighbor_coord not in grid:
            continue
        neighbors.append(neighbor_coord)

    return neighbors


def _walk_region(loc, grid):

    target_char = grid[loc]

    region = {loc}
    visited = {loc}

    queue = list(_neighbors(loc, grid))

    while queue:
        curr = queue.pop()
        visited.add(curr)
        curr_char = grid[curr]
        if curr_char != target_char:
            continue

        region.add(curr)
        for n in _neighbors(curr, grid):
            if n in visited:
                continue
            queue.append(n)


    return region


def _parse_regions(grid):
    all_locs = list(grid.keys())
    all_locs_in_a_region = set()

    regions = list()

    while all_locs:
        loc = all_locs.pop()
        if loc in all_locs_in_a_region:
            continue

        region = _walk_region(loc, grid)
        regions.append(region)
        for rloc in region:
            all_locs_in_a_region.add(rloc)

    assert all_locs_in_a_region == set(grid.keys())
    return regions


def _parse_map(stuff):
    grid = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    return grid


def _score_region(region, grid):
    target_char = grid[list(region)[0]]

    area = len(region)
    perim = 0

    for rloc in region:
        rperim = 4
        for n in _neighbors(rloc, grid):
            if n in region:
                rperim -= 1
        perim += rperim

    return area*perim



@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    grid = _parse_map(stuff)
    regions = _parse_regions(grid)
    return sum(_score_region(region, grid) for region in regions)


def _get_perimeter_groups(region, foochar):
    perimeter_sub_points = list()

    for lx, ly in region:
        # check above neighbor
        if (lx, ly-1) not in region:
            perimeter_sub_points.append((lx, ly, 'u'))
            perimeter_sub_points.append((lx+1, ly, 'u'))

        # check right neighbor
        if (lx+1, ly) not in region:
            perimeter_sub_points.append((lx+1, ly, 'r'))
            perimeter_sub_points.append((lx+1, ly+1, 'r'))

        # check below neighbor
        if (lx, ly+1) not in region:
            perimeter_sub_points.append((lx, ly+1, 'd'))
            perimeter_sub_points.append((lx+1, ly+1, 'd'))

        # check left neighbor
        if (lx-1, ly) not in region:
            perimeter_sub_points.append((lx, ly, 'l'))
            perimeter_sub_points.append((lx, ly+1, 'l'))


    # all the points of all perimeters are in perimeter_sub_points
    # need to group them into separate perimeter groups

    def _is_adjacent(p1, p2):
        dx = abs(p1[0]-p2[0])
        dy = abs(p1[1]-p2[1])
        return dx + dy == 1

    perimeter_groups = []
    for point in perimeter_sub_points:
        if not perimeter_groups:
            perimeter_groups.append(set([point]))
            continue

        did_add = False
        for group in perimeter_groups:
            if any(_is_adjacent(point, other) for other in group):
                group.add(point)
                did_add = True
                break

        if not did_add:
            perimeter_groups.append(set([point]))


    while True:
        did_merge = False
        for group_a, group_b in combinations(perimeter_groups, 2):
            if any(_is_adjacent(a, b) for a in group_a for b in group_b):
                while group_a:
                    group_b.add(group_a.pop())
                did_merge = True
                break
        if not did_merge:
            break
        else:
            perimeter_groups = [p for p in perimeter_groups if p]

    # print(f'\nGroups in region with char {foochar}')
    # for i, p in enumerate(perimeter_groups):
    #     print(f'{i}: {len(p)} points: {p}')

    return perimeter_groups


def _expand_region(region, grid):
    target_char = grid[list(region)[0]]
    new_grid = []

    minx, maxx = min(c[0] for c in grid.keys()), max(c[0] for c in grid.keys())
    miny, maxy = min(c[1] for c in grid.keys()), max(c[1] for c in grid.keys())

    for y in range(miny, maxy+1):
        line = ''
        for x in range(minx, maxx+1):
            for _ in range(2):
                line += target_char if (x,y) in region else '.'
        new_grid.append(line)
        new_grid.append(line)

    # print('Expanded region')
    # for line in new_grid:
    #     print(line)

    expanded_region = set()
    for y, line in enumerate(new_grid):
        for x, char in enumerate(line):
            if char == target_char:
                expanded_region.add((x,y))

    return expanded_region


def _is_adjacent(p1, p2):
    dx = abs(p1[0]-p2[0])
    dy = abs(p1[1]-p2[1])
    return dx + dy == 1


def _matches(ptest, segtest):
    if not any(_is_adjacent(ptest, pseg) for pseg in segtest):
        return False
    # it's adjacent to at least 1 in the segment
    # now check if it's inline with all in the segment
    if {ptest[0]} == {x for x,_,_ in segtest} and {ptest[2]} == {d for _,_,d in segtest}:
        return True
    if {ptest[1]} == {y for _,y,_ in segtest} and {ptest[2]} == {d for _,_,d in segtest}:
        return True
    return False


def _build_segment(group):

    # pick any arbitrary point
    segment = [group.pop()]

    while True:
        found_another = False

        for point in group:
            if _matches(point, segment):
                segment.append(point)
                found_another = True
                break

        if found_another:
            group = [g for g in group if g not in segment]
        else:
            break

    return segment, group




def _count_line_segments(group):
    group = list(group)

    # print(f'\nlooking at {group}')
    # print('-------------')
    # for g in group:
    #     print(g)
    # print('-------------')

    def _preview_segments(new_point, segs):
        # print(f'\nnew point {new_point}')
        for i, seg in enumerate(segs):
            pass
            # print(f'{i+1} -- {seg}')

    segments = []
    while group:
        new_seg, group = _build_segment(group)
        segments.append(new_seg)

    # print(f'found {len(segments)} sides in perimeter group')
    return len(segments)


def _count_sides(region, grid):
    """
    AAAAAA
    AAABBA
    AAABBA
    ABBAAA
    ABBAAA
    AAAAAA

    counts 11 sides for A because of the criss-cross at the corner Bs
    """
    # print('')
    expanded_region = _expand_region(region, grid)
    perimeter_groups = _get_perimeter_groups(expanded_region, grid[list(region)[0]])
    # for each of the perimeters in perimeter groups, group the lines into line segments
    # and count those, and return the total
    sides = sum(_count_line_segments(group) for group in perimeter_groups)
    # print(f'found {sides=} region')
    return sides


def _score_region_v2(region, grid):
    letter = grid[list(region)[0]]

    area = len(region)
    sides = _count_sides(region, grid)

    # print(f'Region of {letter} plants with {area=} and {sides=}')
    return area * sides


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    grid = _parse_map(stuff)
    regions = _parse_regions(grid)
    return sum(_score_region_v2(region, grid) for region in regions)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    # too low 932778
    part_two(stuff)

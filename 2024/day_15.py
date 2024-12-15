import types
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 15
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

BOT = '@'
WALL = '#'
SPACE = '.'
ROCK = 'O'


def _parse_directions(raw_input: list[str]) -> list[str]:
    empty_line_ix = raw_input.index('')
    directions = []
    for line in raw_input[empty_line_ix+1:]:
        directions.extend(char for char in line)
    return directions


def _parse_grid(raw_input: list[str]) -> dict[tuple[int, int], str]:
    empty_line_ix = raw_input.index('')

    grid = dict()
    for y, line in enumerate(raw_input[:empty_line_ix]):
        for x, char in enumerate(line):
            grid[(x, y)] = char

    return grid


def _get_coord_of_bot(grid):
    for coord, char in grid.items():
        if char == BOT:
            return coord
    raise ValueError("Bot not found")


def _move_bot(grid, direction):
    bx, by = _get_coord_of_bot(grid)

    dx, dy = 0, 0
    if direction == '>':
        dx = 1
    elif direction == '<':
        dx = -1
    elif direction == '^':
        dy = -1
    elif direction == 'v':
        dy = 1

    is_blocked = False
    open_space = None
    rocks_to_move = []

    for i in int_stream():
        testchar = grid.get((bx+(i*dx), by+(i*dy)))
        if testchar == ROCK:
            rocks_to_move.append((bx+i, by))
        elif testchar == WALL:
            is_blocked = True
            break
        elif testchar == SPACE:
            open_space = (bx+(i*dx), by+(i*dy))
            break

    if is_blocked:
        return grid

    assert open_space is not None, "Open space not found when expected"

    grid[(bx, by)] = SPACE
    if rocks_to_move:
        grid[open_space] = ROCK
        grid[(bx+dx, by+dy)] = BOT
    else:
        grid[open_space] = BOT

    return grid


def _print_grid(grid):
    print('')
    max_x = max(x for x, y in grid.keys())
    max_y = max(y for x, y in grid.keys())
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(grid.get((x, y), ' '), end='')
        print('')


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)
    directions = _parse_directions(raw_input)

    for direction in directions:
        grid = _move_bot(grid, direction)
        # _print_grid(grid)

    foo = 0
    for coord, char in grid.items():
        x, y = coord
        if char == ROCK:
            foo += 100*y + x
    return foo



# -----------


def _parse_grid_v2(raw_input: list[str]) -> dict[tuple[int, int], str]:
    empty_line_ix = raw_input.index('')

    raw_map = raw_input[:empty_line_ix]
    raw_map_expanded = []
    for line in raw_map:
        newline = ''
        for char in line:
            if char == WALL:
                newline += WALL + WALL
            elif char == SPACE:
                newline += SPACE + SPACE
            elif char == BOT:
                newline += BOT + SPACE
            elif char == ROCK:
                newline += '[]'
            else:
                raise ValueError(f"Unexpected character {char}")
        raw_map_expanded.append(newline)

    grid = dict()
    for y, line in enumerate(raw_map_expanded):
        for x, char in enumerate(line):
            grid[(x, y)] = char

    _print_grid(grid)
    return grid


def _move_bot_v2(grid, direction):
    bx, by = _get_coord_of_bot(grid)

    dx, dy = 0, 0
    if direction == '>':
        dx = 1
    elif direction == '<':
        dx = -1
    elif direction == '^':
        dy = -1
    elif direction == 'v':
        dy = 1

    coords_of_rocks = set()

    testx, testy = bx+dx, by+dy
    testchar = grid.get((testx, testy))
    if testchar == '[':
        # this is the left half of the rock
        coords_of_rocks.add((testx, testy, '['))
        # also record the right half of the rock
        coords_of_rocks.add((testx+1, testy, ']'))
    elif testchar == ']':
        # this is the right half of the rock
        coords_of_rocks.add((testx, testy, ']'))
        # also record the left half of the rock
        coords_of_rocks.add((testx-1, testy, '['))
    elif testchar == WALL:
        # we know we're blocked, can just return early
        return grid
    elif testchar == SPACE:
        # we know we can move
        grid[(bx, by)] = SPACE
        grid[(testx, testy)] = BOT
        return grid

    # If we're here, we're attempting to move a rock.
    # Check beyond the rocks to see what's happening.
    while True:
        more_rocks_to_add = set()
        for rx, ry, _ in coords_of_rocks:
            tx = rx+dx
            ty = ry+dy
            testchar = grid.get((tx, ty))
            if testchar == '[':
                more_rocks_to_add.add((tx, ty, '['))
                more_rocks_to_add.add((tx+1, ty, ']'))
            elif testchar == ']':
                more_rocks_to_add.add((tx, ty, ']'))
                more_rocks_to_add.add((tx-1, ty, '['))
            elif testchar == WALL:
                return grid
            elif testchar == SPACE:
                continue
        # remove from more_rocks_to_add any rocks that are already in coords_of_rocks
        more_rocks_to_add = more_rocks_to_add - coords_of_rocks
        if not more_rocks_to_add:
            break
        coords_of_rocks.update(more_rocks_to_add)

    # If we're here, we can move the rocks and bot
    if direction == '^':
        coords_of_rocks = sorted(coords_of_rocks, key=lambda c: c[1], reverse=True)
    elif direction == 'v':
        coords_of_rocks = sorted(coords_of_rocks, key=lambda c: c[1])
    elif direction == '<':
        coords_of_rocks = sorted(coords_of_rocks, key=lambda c: c[0], reverse=True)
    elif direction == '>':
        coords_of_rocks = sorted(coords_of_rocks, key=lambda c: c[0])
    else:
        raise ValueError(f"Unexpected direction {direction}")

    newly_updated_coords = set()

    for rx, ry, char in coords_of_rocks:
        grid[(rx+dx, ry+dy)] = char
        newly_updated_coords.add((rx+dx, ry+dy))

    for rx, ry, _ in coords_of_rocks:
        if (rx, ry) in newly_updated_coords:
            continue
        grid[(rx, ry)] = SPACE

    grid[(bx, by)] = SPACE
    grid[(bx+dx, by+dy)] = BOT

    return grid



@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid_v2(raw_input)
    directions = _parse_directions(raw_input)

    for direction in directions:
        grid = _move_bot_v2(grid, direction)
        # _print_grid(grid)

    _print_grid(grid)
    foo = 0
    for coord, char in grid.items():
        x, y = coord
        if char == '[':
            foo += 100*y + x
    return foo

def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import bidirectional_range, nested_iterable

DAY = 22
YEAR = 2022

PART_ONE_DESCRIPTION = "password based on coords of flat map"
PART_ONE_ANSWER = 126350

PART_TWO_DESCRIPTION = "password based on coords of cube net map"
PART_TWO_ANSWER = 129339

VOID = "%"
WALL = "#"


def _get_teleporter():
    """Part 2 delivers the realization that the bizarre 2D map is actually rendering a cube as
    a 2D net. When you walk off a section of the cube into the "void", you are actually moving
    onto an adjacent face of the cube, pointing in a different direction (w/r/t the original
    view of the 2D map).

    This builds a "teleporter" which maps "voids" along the edge of a cube net (when you walk
    off an edge) to the internal coordinates they corresponds to on the adjacent face of the
    cube, and the new direction you'll be facing after wrapping to the next face.

    This is very specific to my own input, and the edge labels are based on my own handwritten
    sketch of my input's cube net. This certainly won't work on somebody else's input unless
    they have a net that's the same shape as mine:

          [][]
          []
        [][]
        []

    This is crazy tedious but I can't think of a more clever way to do it."""

    teleporter = dict()

    # Connect edge A1 to A2
    # A1 void runs vertically, x = 100, y from 50-99, facing RIGHT when you go in.
    # Connects to A2 internally, at y = 49, x from 100-149, facing UP when you come out.
    a1_void_range = ((100, y) for y in range(50, 100))
    a2_internal_range = ((x, 49) for x in range(100, 150))
    for a1, a2 in zip(a1_void_range, a2_internal_range):
        teleporter[(a1, "r")] = (a2, "u")

    assert len(teleporter) == 50

    # Connect edge A2 to A1
    # A2 void runs horizontally, y = 50, x from 100-149, facing DOWN when you go in.
    # Connects to A1 internally, at x = 99, y from 50-99, facing LEFT when you come out.
    a2_void_range = ((x, 50) for x in range(100, 150))
    a1_internal_range = ((99, y) for y in range(50, 100))
    for a2, a1 in zip(a2_void_range, a1_internal_range):
        teleporter[(a2, "d")] = (a1, "l")

    assert len(teleporter) == 100

    # Connect edge B1 to B2
    # B1 void runs vertically, x = 49, y from 99-50, facing LEFT when you go in.
    # Connects to B2 internally, at y = 100, x from 49-0, facing DOWN when you come out.
    b1_void_range = ((49, y) for y in bidirectional_range(99, 49))
    b2_internal_range = ((x, 100) for x in bidirectional_range(49, -1))
    for b1, b2 in zip(b1_void_range, b2_internal_range):
        teleporter[(b1, "l")] = (b2, "d")

    assert len(teleporter) == 150

    # Connect edge B2 to B1
    # B2 void runs horizontally, y = 99, x from 49-0, facing UP when you go in.
    # Connects to B1 internally, at x = 50, y from 99-50, facing RIGHT when you come out.
    b2_void_range = ((x, 99) for x in bidirectional_range(49, -1))
    b1_internal_range = ((50, y) for y in bidirectional_range(99, 49))
    for b2, b1 in zip(b2_void_range, b1_internal_range):
        teleporter[(b2, "u")] = (b1, "r")

    assert len(teleporter) == 200

    # Connect edge C1 to C2
    # C1 void runs vertically, x = 100, y from 100-149, facing RIGHT when you go in.
    # Connects to C2 internally, at x = 149, y from 49-0, facing LEFT when you come out.
    c1_void_range = ((100, y) for y in range(100, 150))
    c2_internal_range = ((149, y) for y in bidirectional_range(49, -1))
    for c1, c2 in zip(c1_void_range, c2_internal_range):
        teleporter[(c1, "r")] = (c2, "l")

    assert len(teleporter) == 250

    # Connect edge C2 to C1
    # C2 void runs vertically, x = 150, y from 49-0, facing RIGHT when you go in.
    # Connects to C1 internally, at x = 99, y from 100-149, facing LEFT when you come out.
    c2_void_range = ((150, y) for y in bidirectional_range(49, -1))
    c1_internal_range = ((99, y) for y in range(100, 150))
    for c2, c1 in zip(c2_void_range, c1_internal_range):
        teleporter[(c2, "r")] = (c1, "l")

    assert len(teleporter) == 300

    # Connect edge D1 to D2
    # D1 void runs vertically, x = 50, y from 199-150, facing RIGHT when you go in.
    # Connects to D2 internally, at y = 149, x from 99-50, facing UP when you come out.
    d1_void_range = ((50, y) for y in bidirectional_range(199, 149))
    d2_internal_range = ((x, 149) for x in bidirectional_range(99, 49))
    for d1, d2 in zip(d1_void_range, d2_internal_range):
        teleporter[(d1, "r")] = (d2, "u")

    assert len(teleporter) == 350

    # Connect edge D2 to D1
    # D2 void runs horizontally, y = 150, x from 99-50, facing DOWN when you go in.
    # Connects to D1 internally, x = 49, y from 199-150, facing LEFT when you come out.
    d2_void_range = ((x, 150) for x in bidirectional_range(99, 49))
    d1_internal_range = ((49, y) for y in bidirectional_range(199, 149))
    for d2, d1 in zip(d2_void_range, d1_internal_range):
        teleporter[(d2, "d")] = (d1, "l")

    assert len(teleporter) == 400

    # Connect edge E1 to E2
    # E1 void runs horizontally, y = 200, x from 0-49, facing DOWN when you go in.
    # Connects to E2 internally, y = 0, x from 100-149, facing DOWN when you come out.
    e1_void_range = ((x, 200) for x in range(0, 50))
    e2_internal_range = ((x, 0) for x in range(100, 150))
    for e1, e2 in zip(e1_void_range, e2_internal_range):
        teleporter[(e1, "d")] = (e2, "d")

    assert len(teleporter) == 450

    # Connect edge E2 to E1
    # E2 void runs horizontally, y = -1, x from 100-149, facing UP when you go in.
    # Connects to E1 internally, y = 199, x from 0-49, facing UP when you come out.
    e2_void_range = ((x, -1) for x in range(100, 150))
    e1_internal_range = ((x, 199) for x in range(0, 50))
    for e2, e1 in zip(e2_void_range, e1_internal_range):
        teleporter[(e2, "u")] = (e1, "u")

    assert len(teleporter) == 500

    # Connect edge F1 to F2
    # F1 void runs horizontally, y = -1, x from 50-99, facing UP when you go in.
    # Connects to F2 internally, x = 0, y from 150-199, facing RIGHT when you come out.
    f1_void_range = ((x, -1) for x in range(50, 100))
    f2_internal_range = ((0, y) for y in range(150, 200))
    for f1, f2 in zip(f1_void_range, f2_internal_range):
        teleporter[(f1, "u")] = (f2, "r")

    assert len(teleporter) == 550

    # Connect edge F2 to F1
    # F2 void runs vertically, x = -1, y from 150-199, facing LEFT when you go in.
    # Connects to F1 internally, y = 0, x from 50-99, facing DOWN when you come out.
    f2_void_range = ((-1, y) for y in range(150, 200))
    f1_internal_range = ((x, 0) for x in range(50, 100))
    for f2, f1 in zip(f2_void_range, f1_internal_range):
        teleporter[(f2, "l")] = (f1, "d")

    assert len(teleporter) == 600

    # Connect edge G1 to G2
    # G1 void runs vertically, x = 49, y from 0-49, facing LEFT when you go in.
    # Connects to G2 internally, x = 0, y from 149-100, facing RIGHT when you come out.
    g1_void_range = ((49, y) for y in range(0, 50))
    g2_internal_range = ((0, y) for y in bidirectional_range(149, 99))
    for g1, g2 in zip(g1_void_range, g2_internal_range):
        teleporter[(g1, "l")] = (g2, "r")

    assert len(teleporter) == 650

    # Connect G2 to G1
    # G2 void runs vertically, x = -1, y from 149-100, facing LEFT when you go in.
    # Connects to G1 internally, x = 50, y from 0-49, facing RIGHT when you come out.
    g2_void_range = ((-1, y) for y in bidirectional_range(149, 99))
    g1_internal_range = ((50, y) for y in range(0, 50))
    for g2, g1 in zip(g2_void_range, g1_internal_range):
        teleporter[(g2, "l")] = (g1, "r")

    assert len(teleporter) == 700

    # Return the dang thing.
    return teleporter


def _get_map(raw_input):
    """Parses the raw input and returns a map of coordinates to the value at that coordinate.
    Any cell which is either a literal space, or is outside the bounds of the map, is a "void"
    and indicates that you need to wrap around back into the grid somewhere."""

    magic_map = defaultdict(lambda: VOID)

    map_portion = raw_input[:200]

    max_width = 0
    for line in map_portion:
        max_width = max([max_width, len(line)])

    for x, y in nested_iterable(range(max_width), range(200)):
        try:
            cell = map_portion[y][x]
            magic_map[(x, y)] = VOID if cell == " " else cell
        except IndexError:
            magic_map[(x, y)] = VOID

    return magic_map


def _get_instructions(raw_input):
    """Parses the raw input for the "instructions" portion, and returns a list of either
    characters R/L to indicate an in-place turn to the right or left, or an integer which
    indicates how many steps forward to take in the direction you're currently facing."""

    turns = set("RL")

    instructions = list()

    buffer = list()
    for c in raw_input[201]:
        if c in turns:
            # If we're turning, turn the numberic characters in the buffer into an integer
            # for number of steps to take, and then add the turn itself after. Clear the buffer.
            instructions.append(int("".join(buffer)))
            instructions.append(c)
            buffer = list()
        else:
            # Add the numeric-as-string digit to a buffer which we'll turn into an integer later
            # once we're done fully reading the number.
            buffer.append(c)

    # If we ended on a digit, we still have stuff left in the buffer. Number-ify it and add it.
    if buffer:
        instructions.append(int("".join(buffer)))

    return instructions


def _new_direction(curr_dir, turn):
    """Given a current direction you're facing, return the next directiony you'll be facing
    after either a right or left turn."""

    if turn == "R":
        return {"r": "d", "d": "l", "l": "u", "u": "r"}[curr_dir]
    else:
        return {"r": "u", "u": "l", "l": "d", "d": "r"}[curr_dir]


def _get_password(row, column, facing):
    """Get the password based on your current (x,y) coord and the direction you're facing."""

    password = (1000 * (column + 1)) + (4 * (row + 1))
    password += {"r": 0, "d": 1, "l": 2, "u": 3}[facing]
    return password


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    magic_map = _get_map(stuff)
    instructions = _get_instructions(stuff)

    max_width = max(x for x, _ in magic_map.keys()) + 1
    max_height = max(y for _, y in magic_map.keys()) + 1

    # Part 1 "walk" function which moves you 1 unit in the specified direction.
    def _walk(curr_dir, x, y):
        if curr_dir == "r":
            return (x + 1) % max_width, y
        if curr_dir == "l":
            return (x - 1) % max_width, y
        if curr_dir == "u":
            return x, (y - 1) % max_height
        if curr_dir == "d":
            return x, (y + 1) % max_height
        raise ValueError(curr_dir)

    # Start coord and direction
    dir = "r"
    x, y = 0, 0
    for x in range(max_width):
        if magic_map[(x, 0)] not in (VOID, WALL):
            break

    for instruction in instructions:
        if isinstance(instruction, str):
            dir = _new_direction(dir, instruction)
            continue

        # Walk N steps in the direction you're currently facing.
        for _ in range(instruction):

            # nx, ny are candidate next coords we'll be in
            nx, ny = _walk(dir, x, y)

            # If we're stepping into the void, keep going that direction until we wrap around
            # (which we'll know when the cell is not a VOID cell). This doesn't count as any
            # extra steps; think of it as teleporting through the void until you come out.
            if magic_map[(nx, ny)] == VOID:
                candidate_next_cell = VOID
                while candidate_next_cell == VOID:
                    nx, ny = _walk(dir, nx, ny)
                    candidate_next_cell = magic_map[(nx, ny)]

            # If our next step would cause us to run into a wall, stop walking this way.
            if magic_map[(nx, ny)] == WALL:
                break

            # Otherwise we can keep walking this way, update our current position.
            x, y = nx, ny

    return _get_password(x, y, dir)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    magic_map = _get_map(stuff)
    instructions = _get_instructions(stuff)
    teleporter = _get_teleporter()

    # Part 2 "walk" function which moves you 1 unit in the specified direction. If you step into
    # a void, use the teleporter to teleport you to the corresponding position back inside the
    # map, and also returns the new direction you're facing.
    def _move(curr_dir, x, y):
        if curr_dir == "r":
            nx, ny = x + 1, y
        elif curr_dir == "l":
            nx, ny = x - 1, y
        elif curr_dir == "u":
            nx, ny = x, y - 1
        elif curr_dir == "d":
            nx, ny = x, y + 1
        else:
            raise ValueError(curr_dir)

        # You'll keep facing the way you're already moving unless...
        next_dir = curr_dir

        # ... you walked into the void. Teleport back onto the map at the correct location, and
        # update which direction you'll be facing when you land.
        if magic_map[(nx, ny)] == VOID:
            teleported_coord, next_dir = teleporter[((nx, ny), curr_dir)]
            nx, ny = teleported_coord
            curr_dir = next_dir

        return (nx, ny), next_dir

    # Start coord (from above) and direction
    x, y = 50, 0
    dir = "r"

    for instruction in instructions:
        if isinstance(instruction, str):
            dir = _new_direction(dir, instruction)
            continue

        # Walk N steps in the direction you're currently facing.
        for _ in range(instruction):
            next_coord, next_dir = _move(dir, x, y)
            nx, ny = next_coord

            # If our next step would cause us to run into a wall, stop walking this way.
            if magic_map[(nx, ny)] == WALL:
                break

            # Otherwise we can keep walking this way, update our current position and the
            # direction we're facing in case we walked from one face of the cube to another.
            x, y = nx, ny
            dir = next_dir

    return _get_password(x, y, dir)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    raw_input = get_input(input_file)

    part_one(raw_input)
    part_two(raw_input)

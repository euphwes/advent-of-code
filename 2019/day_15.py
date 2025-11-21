import curses
import msvcrt
import sys
from collections.abc import Generator

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.structures import get_neighbors_of_dict_based

from .intcode import InputNotAvailableException, IntcodeComputer

DAY = 15
YEAR = 2019

PART_ONE_DESCRIPTION = "fewest steps to reach the oxygen system from start"
PART_ONE_ANSWER = 254

PART_TWO_DESCRIPTION = "how long to fill the map with oxygen"
PART_TWO_ANSWER = 268


Coord = tuple[int, int]

DROID = "O"
WALL = "█"
OPEN = "░"
OXYGEN = "X"
START = "S"


def _run(
    program: list[int],
    program_input: Generator[int] | None = None,
) -> Generator[list[int]]:
    computer = IntcodeComputer()
    while True:
        try:
            computer.execute(
                program,
                program_input=[next(program_input)] if program_input else None,
            )
            break
        except InputNotAvailableException:
            yield computer.get_all_output()

    yield computer.get_all_output()


def arrow_keys(direction_buffer: list[int]) -> Generator[int]:
    """Yield codes corresponding to arrow key pushes.

    Mirrors everything for curses.

    Yields 1 for up, 2 for down, 3 for left, 4 for right

    And also puts the most recent direction into the buffer.
    """
    mapping = {
        b"H": 2,  # up
        b"P": 1,  # down
        b"K": 4,  # left
        b"M": 3,  # right
    }
    while True:
        # Use q to quit
        ch = msvcrt.getch()
        if ch == b"q":
            sys.exit(0)
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            if ch2 in mapping:
                while direction_buffer:
                    direction_buffer.pop()
                direction_buffer.append(mapping[ch2])
                yield mapping[ch2]


def _render(stdscr: curses.window, screen: dict[Coord, str]) -> None:
    min_x = min(x for x, _ in screen)
    max_x = max(x for x, _ in screen)
    min_y = min(y for _, y in screen)
    max_y = max(y for _, y in screen)
    WIDTH = max_x - min_x
    HEIGHT = max_y - min_y

    stdscr.erase()

    for c, t in screen.items():
        x, y = c
        if (x, y) == (0, 0) and t != DROID:
            t = START
        x = WIDTH - x
        y = HEIGHT - y
        stdscr.addch(y, x, t, curses.color_pair(0))

    stdscr.refresh()


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)  # noqa: RET503
def part_one(raw_input: list[str], *, render: bool = True) -> int | str | None:
    # I manually explored the maze by piping keyboard input into the Intcode
    # program, gradually exploring and uncovering the full maze and finding
    # the oxygen system. Then I manually counted and found the shortest path
    # from the start to the oxygen system.
    return 254

    # Set up a curses window in case we want to render the game.
    stdscr = None

    if render:
        stdscr = curses.initscr()
        stdscr.clear()

        curses.curs_set(0)
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            curses.init_pair(2, curses.COLOR_BLUE, -1)
            curses.init_pair(3, curses.COLOR_YELLOW, -1)
            curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    program = [int(x) for x in raw_input[0].split(",")]

    # Hold the current state of the screen (the tile at a given coordinate)
    screen: dict[Coord, str] = {
        (0, 0): DROID,
    }
    # Hold where the robot currently is
    x, y = (0, 0)
    oxygen_coord: Coord | None = None

    # Also hold which direction we went
    direction_buffer = []

    for output in _run(program, arrow_keys(direction_buffer)):
        assert len(output) == 1
        result = output.pop()

        last_direction = direction_buffer[-1]

        if result == 0:
            # movement not successful aka that direction is a wall
            if last_direction == 1:
                screen[(x, y - 1)] = WALL
            elif last_direction == 2:
                screen[(x, y + 1)] = WALL
            elif last_direction == 3:
                screen[(x - 1, y)] = WALL
            else:
                screen[(x + 1, y)] = WALL
        elif result == 1:
            # movement successful, open space
            # The droid's previous location is open space
            screen[(x, y)] = OPEN
            if last_direction == 1:
                y -= 1
            elif last_direction == 2:
                y += 1
            elif last_direction == 3:
                x -= 1
            else:
                x += 1
            screen[(x, y)] = DROID
            if oxygen_coord and (x, y) != oxygen_coord:
                screen[oxygen_coord] = OXYGEN
        elif result == 2:
            # movement successful, oxygen found
            # The droid's previous location is open space
            screen[(x, y)] = OPEN
            if last_direction == 1:
                y -= 1
            elif last_direction == 2:
                y += 1
            elif last_direction == 3:
                x -= 1
            else:
                x += 1
            screen[(x, y)] = DROID
            oxygen_coord = (x, y)
            print(f"found oxygen at {(x, y)}")
        else:
            raise ValueError(result)

        if render:
            assert stdscr is not None
            _render(stdscr, screen)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    # I saved the full rendered map after manually exploring it.
    # Read the map into a dictionary of coordinates that detail the walls
    # and the open spaces.
    WALL = "#"
    SPACE = " "

    start: Coord | None = None
    maze: dict[Coord, str] = {}

    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            assert char in ("X", SPACE, WALL), f"{char} value unexpected"
            if char == "X":
                start = (x, y)
                maze[start] = SPACE
            else:
                maze[(x, y)] = char

    assert start is not None

    # We basically want to flood-fill the entire map from the
    # oxygen system (the start position), and the oxygen spreads
    # from a spot to any unoccupied spot in 1 time step. This means
    # we can just do a standard BFS to count the distance from the
    # start to every cell, and the distance to the cell that's the
    # furthest away is how long it'll take to fill the maze with oxygen.

    distance_to_cell: dict[Coord, int] = {}

    queue = [(start, 0)]
    while queue:
        curr_coord, steps = queue.pop(0)
        if curr_coord in distance_to_cell:
            continue

        distance_to_cell[curr_coord] = steps

        cx, cy = curr_coord
        for neighbor, neighbor_coord in get_neighbors_of_dict_based(
            cx,
            cy,
            maze,
            include_diagonals=False,
            with_coords=True,
        ):
            if neighbor == WALL:
                continue
            queue.append((neighbor_coord, steps + 1))

    return max(distance_to_cell.values())


def run(input_file: str) -> None:
    part_one(get_input(input_file), render=True)
    part_two(get_input(input_file.replace("day15", "day15_map")))

import curses
from collections.abc import Generator
from time import sleep

from util.decorators import aoc_output_formatter
from util.input import get_input

from .intcode import InputNotAvailableException, IntcodeComputer

DAY = 13
YEAR = 2019

PART_ONE_DESCRIPTION = "number of blocks on the screen"
PART_ONE_ANSWER = 251

PART_TWO_DESCRIPTION = "score once all blocks are broken"
PART_TWO_ANSWER = 12779


Coord = tuple[int, int]

BALL = "○"
WALL = "█"
BLOCK = "░"
PADDLE = "▔"
EMPTY = " "


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


def _control_joystick(screen: dict[Coord, str]) -> Generator[int]:
    """Provide inputs to the program to play the breakout game.

    Basically react like a human would by trying to keep the paddle under
    the ball. If the ball is left of the paddle, move left. If the ball
    is right of the paddle, move right.
    """
    while True:
        if not screen:
            yield 0
            continue

        ball_x = next(c[0] for c, t in screen.items() if t == BALL)
        paddle_x = next(c[0] for c, t in screen.items() if t == PADDLE)

        if ball_x < paddle_x:
            yield -1
        elif ball_x > paddle_x:
            yield 1
        else:
            yield 0


def _render(stdscr: curses.window, screen: dict[Coord, str], score: int) -> None:
    sleep(0.01)
    min_x = min(x for x, _ in screen)
    max_x = max(x for x, _ in screen)
    WIDTH = max_x - min_x

    color_map = {
        BALL: curses.color_pair(1),
        WALL: curses.color_pair(0),
        BLOCK: curses.color_pair(2),
        PADDLE: curses.color_pair(3),
        EMPTY: curses.color_pair(0),
    }

    score_banner = f"             SCORE: {score}"
    remainder = WIDTH - len(score_banner)

    stdscr.addstr(1, 2, f"{score_banner}{' ' * remainder}", curses.color_pair(3))
    stdscr.addstr(2, 2, "▔" * (WIDTH + 1), curses.color_pair(3))
    for c, t in screen.items():
        x, y = c
        x = WIDTH - x + 2
        y = y + 3
        stdscr.addch(y, x, t, color_map[t])

    stdscr.refresh()


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    program = [int(x) for x in raw_input[0].split(",")]
    output = next(_run(program, None))

    # Every 3rd value from the output identifies a tile (the first 2 are coordinates)
    tiles = [t for i, t in enumerate(output) if (i + 1) % 3 == 0]

    # 2 identifies a breakable block tile
    return sum(1 for tile in tiles if tile == 2)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str], *, render: bool = False) -> int | str | None:
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
    program[0] = 2

    # Hold the current state of the screen (the tile at a given coordinate)
    screen: dict[Coord, str] = {}

    score = 0
    for output in _run(program, _control_joystick(screen)):
        # For each frame while running the program, get the output
        # and use that to figure out the state of the arcade cabinet screen.
        while output:
            # 3 values at a time: x,y coordinates, and t is a tile ID
            x, y, tile = output[:3]
            output = output[3:]

            # Special case (-1, 0) means the "tile ID" is actually the score
            if (x, y) == (-1, 0):
                score = tile
                continue

            # Write the correct char to the screen at the coordinates for
            # a given tile ID.
            screen[(x, y)] = {
                0: EMPTY,
                1: WALL,
                2: BLOCK,
                3: PADDLE,
                4: BALL,
            }[tile]

        if render:
            assert stdscr is not None
            _render(stdscr, screen, score)

    return score


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file), render=False)

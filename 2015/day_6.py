from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

DAY = 6
YEAR = 2015

PART_ONE_DESCRIPTION = "number of lights on"
PART_ONE_ANSWER = 400410

PART_TWO_DESCRIPTION = "total light brightness"
PART_TWO_ANSWER = 15343601


def _v1_toggle(x: int) -> int:
    return 0 if x == 1 else 1


def _v1_turn_on(_: int) -> int:
    return 1


def _v1_turn_off(_: int) -> int:
    return 0


def _v2_toggle(x: int) -> int:
    return x + 2


def _v2_turn_on(x: int) -> int:
    return x + 1


def _v2_turn_off(x: int) -> int:
    return max([0, x - 1])


class LightsCommand:
    """Encapsulates an action to be performed on a grid of Christmas lights."""

    # Constants to indicate the action this LightsCommand will enact
    TOGGLE = "toggle"
    TURN_ON = "on"
    TURN_OFF = "off"

    # Constants to indicate which LightsCommand logic version is being used
    COMMAND_V1 = "v1"
    COMMAND_V2 = "v2"

    def __init__(self, input_tokens: list[str], logic_version: str = "v1") -> None:
        # If the first token is 'toggle', that's the command. Shave off the first token.
        if input_tokens[0] == LightsCommand.TOGGLE:
            command = LightsCommand.TOGGLE
            input_tokens = input_tokens[1:]

        # Otherwise, first token is 'turn', in which case the command is either 'on' or 'off'
        # from the next token. Grab that, and shave off the first two token.
        else:
            command = input_tokens[1]
            input_tokens = input_tokens[2:]

        # With the command portion removed, what's left is "<start_x, start_y> through
        # <end_x, end_y>""
        self.start_x, self.start_y = (int(n) for n in input_tokens[0].split(","))
        self.end_x, self.end_y = (int(n) for n in input_tokens[2].split(","))

        self.command_function = {
            LightsCommand.COMMAND_V1: {
                LightsCommand.TOGGLE: _v1_toggle,
                LightsCommand.TURN_ON: _v1_turn_on,
                LightsCommand.TURN_OFF: _v1_turn_off,
            },
            LightsCommand.COMMAND_V2: {
                LightsCommand.TOGGLE: _v2_toggle,
                LightsCommand.TURN_ON: _v2_turn_on,
                LightsCommand.TURN_OFF: _v2_turn_off,
            },
        }[logic_version][command]

    def execute(self, lights: dict[tuple[int, int], int]) -> None:
        """Execute this command.

        Perform the action (turn on, turn off, toggle) this action describes against the range
        of lights that the command specifies.
        """

        for coord in nested_iterable(
            range(self.start_x, self.end_x + 1),
            range(self.start_y, self.end_y + 1),
        ):
            lights[coord] = self.command_function(lights[coord])


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    lights = dict.fromkeys(nested_iterable(range(1000), range(1000)), 0)

    for command in (
        LightsCommand(tokens, LightsCommand.COMMAND_V1)
        for tokens in [line.split() for line in raw_input]
    ):
        command.execute(lights)

    return sum(lights.values())


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    lights = dict.fromkeys(nested_iterable(range(1000), range(1000)), 0)

    for command in (
        LightsCommand(tokens, LightsCommand.COMMAND_V2)
        for tokens in [line.split() for line in raw_input]
    ):
        command.execute(lights)

    return sum(lights.values())


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

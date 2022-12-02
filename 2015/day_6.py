from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input
from util.iter import nested_iterable

#---------------------------------------------------------------------------------------------------

class LightsCommand:
    """ A class that encapsulates an action to be performed on a grid of Christmas lights. The
    action is either 'toggle', 'turn on', or 'turn off', with start and end coordinates. """

    # Constants to indicate the action this LightsCommand will enact
    TOGGLE   = 'toggle'
    TURN_ON  = 'on'
    TURN_OFF = 'off'

    # Constants to indicate which LightsCommand logic version is being used
    COMMAND_V1 = 'v1'
    COMMAND_V2 = 'v2'

    # LightsCommand V1 commands logic
    __v1_toggle   = lambda x: 0 if x == 1 else 1
    __v1_turn_on  = lambda _: 1
    __v1_turn_off = lambda _: 0

    # LightsCommand V2 commands logic
    __v2_toggle   = lambda x: x + 2
    __v2_turn_on  = lambda x: x + 1
    __v2_turn_off = lambda x: max([0, x - 1])

    # Parses two integers from a single string of the form "x,y".
    __parse_int_pair = lambda token: (int(n) for n in token.split(','))

    def __init__(self, input_tokens, logic_version='v1'):
        # If the first token is 'toggle', that's the command. Shave off the first token.
        if input_tokens[0] == LightsCommand.TOGGLE:
            command = LightsCommand.TOGGLE
            input_tokens = input_tokens[1:]

        # Otherwise, first token is 'turn', in which case the command is either 'on' or 'off' from
        # the next token. Grab that, and shave off the first two token.
        else:
            command = input_tokens[1]
            input_tokens = input_tokens[2:]

        # With the command portion removed, what's left is "<start_x,start_y> through <end_x,end_y>"
        self.start_x, self.start_y = LightsCommand.__parse_int_pair(input_tokens[0])
        self.end_x, self.end_y     = LightsCommand.__parse_int_pair(input_tokens[2])

        self.command_function = {
            LightsCommand.COMMAND_V1: {
                LightsCommand.TOGGLE:   LightsCommand.__v1_toggle,
                LightsCommand.TURN_ON:  LightsCommand.__v1_turn_on,
                LightsCommand.TURN_OFF: LightsCommand.__v1_turn_off,
            },
            LightsCommand.COMMAND_V2: {
                LightsCommand.TOGGLE:   LightsCommand.__v2_toggle,
                LightsCommand.TURN_ON:  LightsCommand.__v2_turn_on,
                LightsCommand.TURN_OFF: LightsCommand.__v2_turn_off,
            }
        }[logic_version][command]


    def execute(self, lights):
        """ Executes the command. Lights is a dictionary where the key is the (x,y) coordinate of
        the individual light, and the value is the state of the light. Iterates over the grid of
        lights across the range specified by the start and end coordinates, executing the commands
        function against each light."""

        x_range = range(self.start_x, self.end_x + 1)
        y_range = range(self.start_y, self.end_y + 1)

        for coord in nested_iterable(x_range, y_range):
            lights[coord] = self.command_function(lights[coord])

        return lights

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 6, 1, 'number of lights on', assert_answer=400410)
def part_one(lights, commands):
    for command in commands:
        lights = command.execute(lights)

    return sum(lights.values())


@aoc_output_formatter(2015, 6, 2, 'total light brightness', assert_answer=15343601)
def part_two(lights, commands):
    for command in commands:
        lights = command.execute(lights)

    return sum(lights.values())

#---------------------------------------------------------------------------------------------------

def run(input_file):

    def __new_lights_grid():
        """ Returns a 1000x1000 grid of lights that all start off. """
        lights = dict()
        for coord in nested_iterable(range(1000), range(1000)):
            lights[coord] = 0
        return lights

    commands = [LightsCommand(tokens, LightsCommand.COMMAND_V1) for tokens in get_tokenized_input(input_file, ' ')]
    part_one(__new_lights_grid(), commands)

    commands = [LightsCommand(tokens, LightsCommand.COMMAND_V2) for tokens in get_tokenized_input(input_file, ' ')]
    part_two(__new_lights_grid(), commands)

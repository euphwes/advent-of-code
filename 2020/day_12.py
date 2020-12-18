from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

# lambdas to modify a coordinate value; no-op (do nothing), increment, decrement, negate
NOP = lambda n: n
INC = lambda n: n + 1
DEC = lambda n: n - 1

# Map which dictates how the ship moves for both axes, when using absolute directions
# Keys: N,E,S,W = North, East, South, West
# Values: (x_coord_modifier, y_coord_modifier)
ABS_MOVE_MAP = {
    'N': (NOP, DEC),
    'E': (INC, NOP),
    'S': (NOP, INC),
    'W': (DEC, NOP)
}

# Convert position in degrees to which direction the ship is facing. Converts a relative "forward"
# movement into an absolute direct depending on which way the ship is facing.
DIR_MAP = {
    0:   'N',
    90:  'E',
    180: 'S',
    270: 'W'
}

def __turn(heading, direction, degrees):
    """ Executes a `degrees` turn in the specified direction, and returns the ship's heading after
    the maneuver is complete. """

    if direction == 'L':
        degrees *= -1

    return (heading + degrees) % 360


def __sail(x, y, direction, distance):
    """ Executes sailing in the specified direction, from a starting (x, y) coordinate position.
    Returns the position of the ship when the maneuver is complete. """

    x_coord_modifier, y_coord_modifier = ABS_MOVE_MAP[direction]
    for _ in range(distance):
        x = x_coord_modifier(x)
        y = y_coord_modifier(y)

    return x, y


def __move(x, y, heading, command):
    """ Executes a ship maneuver from the specified starting (x, y) coordinates and heading, and
    returns the position and heading of the ship (as a tuple of (x, y, degrees)) when the maneuver
    is complete. """

    command_code, amount = command[0], int(command[1:])

    # If command is 'R' or 'L', it's a turn. Execute the specified turn, and then return the
    # ship's position (unchanged) and modified heading.
    if command_code in 'RL':
        return x, y, __turn(heading, command_code, amount)

    # The command must be sailing in some direction. If the direction is not absolute (N,E,S,W),
    # the command is "forward", which must be converted into an absolute direction.
    if command_code not in 'NESW':
        command_code = DIR_MAP[heading]

    # Now that we know for sure the absolute direction the ship is sailing, excute the maneuver and
    # return the modified position of the ship, and its unchanged heading.
    x, y = __sail(x, y, command_code, amount)
    return x, y, heading


def __rotate_waypoint_about_ship(x, y, ship_x, ship_y, direction, degrees):
    """ Rotates the waypoint about the ship in the specified direction by the specified amount.
    Returns the position of the waypoint after the maneuver is complete.

    Ex: Rotating (1, 4) about (0, 0) clockwise
        > ( 1,  4)    start (bottom-right quadrant)
        > (-4,  1)    first rotation of 90 deg (bottom-left quadrant)
        > (-1, -4)    second rotation of 90 deg (upper-left quadrant)
        > ( 4, -1)    third rotation of 90 deg (upper-right quadrant)
    """

    # Convert a L rotation to a R rotation, so we can model all rotations as a clockwise rotation.
    if direction == 'L':
        if degrees in (90, 270):
            degrees = (degrees + 180) % 360

    # Break the rotation up into some number of 90 degree increments, and then just repeat the logic
    # for performing a 90 degree clockwise rotation the correct number of times.
    num_90_deg_increments = int(degrees / 90)
    for i, _ in enumerate(range(num_90_deg_increments), 1):
        # Determine x and y coordinate diffs between the waypoint and the ship
        diff_x = x - ship_x
        diff_y = y - ship_y
        # Apply the y and x differences to the x and y coordinates respectively, and negate the
        # x difference coordinate to account for changing quadrants.
        x = ship_x + (diff_y * -1)
        y = ship_y + diff_x

    return x, y


def __move_waypoint(x, y, ship_x, ship_y, command_code, amount):
    """ Executes a waypoint maneuver from the specified starting (x, y) coordinates, using the
    ship's coordinates (ship_x, ship_y) as a reference if necessary and returns the position of the
    waypoint when the maneuver is complete. """

    # If command is 'R' or 'L', it's rotating the waypoint around the ship by the specified number
    # of degrees. Execute the rotation maneuver.
    if command_code in 'RL':
        return __rotate_waypoint_about_ship(x, y, ship_x, ship_y, command_code, amount)

    # The command must be moving the waypoint N,E,S,W in some direction. We can model this as
    return __sail(x, y, command_code, amount)


def __move_ship_to_waypoint(way_x, way_y, ship_x, ship_y, num_times):
    """ Moves the ship to the waypoint the specified number of times, always keeping the waypoint in
    the same position relative to the ship. Returns the ship coordinates and waypoint coordinates
    when the maneuver completes. """

    diff_x = way_x - ship_x
    diff_y = way_y - ship_y

    ship_x = ship_x + (num_times * diff_x)
    ship_y = ship_y + (num_times * diff_y)
    way_x = ship_x + diff_x
    way_y = ship_y + diff_y

    return way_x, way_y, ship_x, ship_y

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 12, 1, 'Manhattan distance from starting point')
def part_one(maneuvers):
    x, y, heading = 0, 0, 90 # facing east to start
    for maneuver in maneuvers:
        x, y, heading = __move(x, y, heading, maneuver)
    return abs(x) + abs(y)


@aoc_output_formatter(2020, 12, 2, 'Manhattan distance from starting point')
def part_two(maneuvers):
    ship_x, ship_y = 0, 0
    way_x, way_y = 10, -1
    for maneuver in maneuvers:
        command_code, amount = maneuver[0], int(maneuver[1:])
        if command_code == 'F':
            way_x, way_y, ship_x, ship_y = __move_ship_to_waypoint(way_x, way_y, ship_x, ship_y, amount)
        else:
            way_x, way_y = __move_waypoint(way_x, way_y, ship_x, ship_y, command_code, amount)

    return abs(ship_x) + abs(ship_y)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

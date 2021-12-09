from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable
from util.structures import get_neighbors_of


#---------------------------------------------------------------------------------------------------

FLOOR = '.'
OPEN_SEAT = 'L'
OCCUPIED_SEAT = '#'


def __visible_neighbors_of(seat_x, seat_y, seating_area):
    """ Returns a generator which yields each seat which is the first visible one in each direction
    from the specified seat. """

    max_x = len(seating_area[0])
    max_y = len(seating_area)

    # lambdas to modify a coordinate value; no-op (do nothing), increment, decrement
    nop = lambda n: n
    inc = lambda n: n + 1
    dec = lambda n: n - 1

    # For each direction from the seat, store a tuple of coordinate modifiers that describe how to
    # traverse the seats from that direction. For example, the upper right diagonal can be traversed
    # by incrementing the x coordinating, and decrementing the y coordinate, from the starting point
    direction_coord_modifiers = [
        (dec, dec),  # upper left diagonal
        (nop, dec),  # up
        (inc, dec),  # upper right diagonal
        (inc, nop),  # right
        (inc, inc),  # lower right diagonal
        (nop, inc),  # down
        (dec, inc),  # lower left diagonal
        (dec, nop),  # left
    ]

    def __check_out_of_bounds(x, y):
        """ Returns if the specified location is out of the bounds of the seating area. """
        if x < 0 or x >= max_x:
            return True
        return y < 0 or y >= max_y

    # For each direction to be traversed, start at the starting seat and ...
    for direction_mods in direction_coord_modifiers:
        x, y = seat_x, seat_y
        x_modifier, y_modifier = direction_mods

        # ... continue moving that direction.
        while True:
            x = x_modifier(x)
            y = y_modifier(y)

            # If the coordinates are out of bounds, there is no neighbor to yield, so go ahead and
            # skip to the next direction.
            if __check_out_of_bounds(x, y):
                break

            # If there's a floor space in these coordinates, keep moving in the specified direction
            # until we hit a seat or are out of bounds.
            if seating_area[y][x] == FLOOR:
                continue

            # Yield this seat and then break, moving onto the next direction
            yield seating_area[y][x]
            break


# Global variable which will determine which of the two above neighbor implementations is used when
# evaluating the seating area
__neighbors_impl = None


def __count_nearby_occupied_seats(seat_x, seat_y, seating_area):
    """ Returns the number of nearby seats which are occupied. """

    neighbors = __neighbors_impl(seat_x, seat_y, seating_area)
    return sum(1 for n in neighbors if n == OCCUPIED_SEAT)


def __count_total_occupied_seats(seating_area):
    """ Returns a count of occupied seats in the seating area. """

    seats_occupied = 0
    for row in seating_area:
        for seat in row:
            if seat == OCCUPIED_SEAT:
                seats_occupied += 1

    return seats_occupied


def __create_blank_seating_area(width, height):
    """ Creates a blank seating area with the provided width and height. """

    return [[None] * width for _ in range(height)]


# Global variable which determine the maximum number of nearby occupied seats somebody in a seat
# will tolerate before vacating the seat.
__MAX_OCCUPIED_NEIGHBORS = None


def __evaluate_seating_area(seating_area):
    """ Evaluates the seating area and determines its state at the next step in time. """

    width = len(seating_area[0])
    height = len(seating_area)

    # Create a new array which hold the state of the seating area at the next step in time
    new_seating_area = __create_blank_seating_area(width, height)

    # Iterate over each seat and evaluate it to determine what its next state will be
    for x, y in nested_iterable(range(width), range(height)):
        seat = seating_area[y][x]

        # Floors will be floors.
        if seat == FLOOR:
            new_seating_area[y][x] = FLOOR
            continue

        # Count the number of nearby occupied seats.
        nearby_occupied_seats = __count_nearby_occupied_seats(x, y, seating_area)

        # If a seat is currently open, it'll become occupied if it has no nearby occupied seats,
        # otherwise it'll remain open.
        if seat == OPEN_SEAT:
            new_seating_area[y][x] = OCCUPIED_SEAT if nearby_occupied_seats == 0 else OPEN_SEAT
            continue

        # If a seat is currently occupied, it'll become open if there are __MAX_OCCUPIED_NEIGHBORS
        # or more in nearby occupied seats, otherwise it will remain occupied.
        if nearby_occupied_seats >= __MAX_OCCUPIED_NEIGHBORS:
            new_seating_area[y][x] = OPEN_SEAT
        else:
            new_seating_area[y][x] = OCCUPIED_SEAT

    return new_seating_area


def __evaluate_seating_area_until_stabilized(seating_area):
    """ Continues evaluating a seating area until the number of occupied seats has stabilized. """

    occupied_seats = __count_total_occupied_seats(seating_area)
    while True:
        seating_area = __evaluate_seating_area(seating_area)
        new_occupied_seats = __count_total_occupied_seats(seating_area)
        if new_occupied_seats == occupied_seats:
            break
        occupied_seats = new_occupied_seats

    return seating_area

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 11, 1, "number of occupied seats")
def part_one(seating_area):

    global __neighbors_impl, __MAX_OCCUPIED_NEIGHBORS
    __neighbors_impl = get_neighbors_of
    __MAX_OCCUPIED_NEIGHBORS = 4

    seating_area = __evaluate_seating_area_until_stabilized(seating_area)
    return __count_total_occupied_seats(seating_area)


@aoc_output_formatter(2020, 11, 2, 'number of occupied seats with new rules')
def part_two(seating_area):

    global __neighbors_impl, __MAX_OCCUPIED_NEIGHBORS
    __neighbors_impl = __visible_neighbors_of
    __MAX_OCCUPIED_NEIGHBORS = 5

    seating_area = __evaluate_seating_area_until_stabilized(seating_area)
    return __count_total_occupied_seats(seating_area)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    seating_area = [list(line) for line in get_input(input_file)]

    part_one(seating_area)
    part_two(seating_area)

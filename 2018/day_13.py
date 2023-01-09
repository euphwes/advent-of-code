from copy import copy
from enum import Enum

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 13
YEAR = 2018

PART_ONE_DESCRIPTION = "x,y coord where the first cart crash occurs"
PART_ONE_ANSWER = "39,52"

PART_TWO_DESCRIPTION = "x,y coord of last cart remaining after all crashes"
PART_TWO_ANSWER = "133,146"


Direction = Enum("Direction", ["Left", "Right", "Up", "Down"])
Turn = Enum("Turn", ["Left", "Straight", "Right"])


class CartCrashException(Exception):
    def __init__(self, cart1, cart2):
        self.position = cart1.coord
        self.cart1 = cart1
        self.cart2 = cart2


class Cart:
    TURN_ORDER = [Turn.Left, Turn.Straight, Turn.Right]

    def __init__(self, initial_char, x, y):
        self.x = x
        self.y = y

        self.direction = {
            "<": Direction.Left,
            ">": Direction.Right,
            "^": Direction.Up,
            "v": Direction.Down,
        }[initial_char]

        self.turn_index = 0

    @property
    def coord(self):
        return f"{self.x},{self.y}"

    def move(self, track, all_carts):
        """Move the cart by 1 unit in the direction it's facing. When it reaches an intersection
        or a track corner, turn the cart. If the cart ends up in the same position as another
        cart, raise a CartCrashException."""

        delta = {
            Direction.Left: (-1, 0),
            Direction.Right: (1, 0),
            Direction.Up: (0, -1),
            Direction.Down: (0, 1),
        }

        dx, dy = delta[self.direction]
        self.x += dx
        self.y += dy

        other_carts = [cart for cart in all_carts if cart is not self]
        for other in other_carts:
            if self.coord == other.coord:
                raise CartCrashException(self, other)

        track_piece = track[self.y][self.x]

        if track_piece == "+":
            self._turn()

        elif track_piece in "/\\":
            self._force_turn(track_piece)

    def _turn(self):
        """Turn the cart to face a new direction at an intersection, where the cart has a
        choice. Every time an intersection is crossed, the cart cycles through going left,
        straight, and then right, in that order."""

        turn = Cart.TURN_ORDER[self.turn_index]
        self.turn_index = (self.turn_index + 1) % len(Cart.TURN_ORDER)

        if turn == Turn.Straight:
            pass

        elif turn == Turn.Left:
            self.direction = {
                Direction.Left: Direction.Down,
                Direction.Down: Direction.Right,
                Direction.Right: Direction.Up,
                Direction.Up: Direction.Left,
            }[self.direction]

        else:
            self.direction = {
                Direction.Down: Direction.Left,
                Direction.Right: Direction.Down,
                Direction.Up: Direction.Right,
                Direction.Left: Direction.Up,
            }[self.direction]

    def _force_turn(self, track_piece):
        """Turn the cart to face a new direction at a track corner, where the cart does not have
        a choice for which way to turn."""

        if track_piece == "/":
            self.direction = {
                Direction.Right: Direction.Up,
                Direction.Up: Direction.Right,
                Direction.Down: Direction.Left,
                Direction.Left: Direction.Down,
            }[self.direction]

        elif track_piece == "\\":
            self.direction = {
                Direction.Left: Direction.Up,
                Direction.Up: Direction.Left,
                Direction.Right: Direction.Down,
                Direction.Down: Direction.Right,
            }[self.direction]


def _initialize_carts(track):
    """Read the initial track state to find where all the carts are, and create Cart instances
    with their starting positions and directions."""

    carts = list()
    carts_icons = set("v^<>")

    for y, row in enumerate(track):
        for x, cell in enumerate(row):
            if cell in carts_icons:
                carts.append(Cart(cell, x, y))

    return carts


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(track):
    carts = _initialize_carts(track)

    while True:
        # I don't actually seem to need to do this to get the right answer, but the problem
        # specifies that carts move in order of top row to bottom, left to right.
        carts.sort(key=lambda cart: cart.x)
        carts.sort(key=lambda cart: cart.y)

        for cart in carts:
            try:
                cart.move(track, carts)
            except CartCrashException as crash:
                # Return the coordination of the first car crash
                return crash.position


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(track):
    carts = _initialize_carts(track)

    while True:
        # I don't actually seem to need to do this to get the right answer, but the problem
        # specifies that carts move in order of top row to bottom, left to right.
        carts.sort(key=lambda cart: cart.x)
        carts.sort(key=lambda cart: cart.y)

        # Iterate over a copy of the carts, because it's problematic to modify the list of carts
        # while iterating over it directly.
        for cart in copy(carts):
            try:
                cart.move(track, carts)
            except CartCrashException as crash:
                # Every time there's a crash, remove the pair of crashed carts from the track.
                carts.remove(crash.cart1)
                carts.remove(crash.cart2)

        if len(carts) == 1:
            return carts[0].coord


# ----------------------------------------------------------------------------------------------


def run(input_file):

    track = get_input(input_file)

    part_one(track)
    part_two(track)

from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple

#---------------------------------------------------------------------------------------------------

@dataclass
class VirusInfo:
    location: Tuple[int, int]
    direction: str


class CellStatus:
    CLEAN = '.'
    WEAKENED = 'W'
    INFECTED = '#'
    FLAGGED = 'F'


# Simple representation of directions the virus can be facing, and functions to apply a turn
# from a given direction and return the new direction/
_DIRECTIONS = 'uldr'

def left_turn(direction):
    return _DIRECTIONS[(_DIRECTIONS.index(direction)+1) % 4]

def right_turn(direction):
    return _DIRECTIONS[(_DIRECTIONS.index(direction)-1) % 4]

def about_face(direction):
    return _DIRECTIONS[(_DIRECTIONS.index(direction)+2) % 4]

def carry_on(direction):
    return direction


def _map_grid(grid):
    """ Return a map of grid coordinate to cell value, from a 2D array representing the grid. """

    # The grid is actually infinite, and all cells start off clean unless otherwise specified
    # in the limited starting area that we already know about.
    grid_map = defaultdict(lambda: CellStatus.CLEAN)

    for y, grid_row in enumerate(grid):
        for x, element in enumerate(grid_row):
            grid_map[(x, y)] = element

    return grid_map



def _get_burst_fn(status_turn_map, state_transition_map, grid_map):
    """ Returns a virus "burst function" that evaluates a virus's behavior based on two configurable
    pieces of info: 1) how the virus changes the direction its facing based on the status of the
    current cell, and 2) how the current cell changes status when the virus leaves, based on its
    current status. """

    def _burst_fn(virus_info):

        current_location_status = grid_map[virus_info.location]
        virus_info.direction = status_turn_map[current_location_status](virus_info.direction)

        grid_map[virus_info.location] = state_transition_map[grid_map[virus_info.location]]
        did_infect = grid_map[virus_info.location] == CellStatus.INFECTED

        x, y = virus_info.location
        virus_info.location = {
            'u': (x, y-1),
            'd': (x, y+1),
            'r': (x+1, y),
            'l': (x-1, y),
        }[virus_info.direction]

        return virus_info, did_infect

    return _burst_fn


def _evaluate_virus_behavior(start_coord, burst_fn, iterations):
    """ Evaluates a virus's behavior with the given burst function for the specified number of
    iterations, and returns the number of bursts where new infection occurred. """

    bursts_where_infection_occurred = 0
    virus_info = VirusInfo(location=start_coord, direction='u')

    for _ in range(iterations):
        virus_info, did_infect = burst_fn(virus_info)
        if did_infect:
            bursts_where_infection_occurred += 1

    return bursts_where_infection_occurred


@aoc_output_formatter(2017, 22, 1, 'bursts where infection occurred v1')
def part_one(grid, start_coord):

    cell_status_turn_map = {
        CellStatus.CLEAN: left_turn,
        CellStatus.INFECTED: right_turn,
    }

    cell_status_transition_map = {
        CellStatus.CLEAN: CellStatus.INFECTED,
        CellStatus.INFECTED: CellStatus.CLEAN,
    }

    burst_fn = _get_burst_fn(
        status_turn_map=cell_status_turn_map,
        state_transition_map=cell_status_transition_map,
        grid_map=_map_grid(grid)
    )

    return _evaluate_virus_behavior(start_coord, burst_fn, 10_000)


@aoc_output_formatter(2017, 22, 2, 'bursts where infection occurred v2')
def part_two(grid, start_coord):

    cell_status_turn_map = {
        CellStatus.CLEAN: left_turn,
        CellStatus.WEAKENED: carry_on,
        CellStatus.INFECTED: right_turn,
        CellStatus.FLAGGED: about_face,
    }

    cell_status_transition_map = {
        CellStatus.CLEAN: CellStatus.WEAKENED,
        CellStatus.WEAKENED: CellStatus.INFECTED,
        CellStatus.INFECTED: CellStatus.FLAGGED,
        CellStatus.FLAGGED: CellStatus.CLEAN,
    }

    burst_fn = _get_burst_fn(
        status_turn_map=cell_status_turn_map,
        state_transition_map=cell_status_transition_map,
        grid_map=_map_grid(grid)
    )

    return _evaluate_virus_behavior(start_coord, burst_fn, 10_000_000)


#---------------------------------------------------------------------------------------------------

def run(input_file):

    grid = get_input(input_file)

    half_width = len(grid[0])//2
    half_height = len(grid)//2
    start_coord = (half_width, half_height)

    part_one(grid, start_coord)
    part_two(grid, start_coord)

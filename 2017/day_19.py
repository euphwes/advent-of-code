from util.decorators import aoc_output_formatter
from util.input import get_input

from dataclasses import dataclass 
from string import ascii_uppercase
from typing import Optional, Tuple

#---------------------------------------------------------------------------------------------------

class TravelDirection:
    UP = 'u'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'


@dataclass
class PipeWalkInfo:
    value: Optional[str]
    coord: Optional[Tuple[int, int]]
    travel_direction: Optional[TravelDirection]
    step_size: int


JUNCTION_PIPE = '+'
VERTICAL_PIPE = '|'

LETTERS = set(ascii_uppercase)


def _get_next_pipewalkinfo(current_coord, map, travel_direction):
    """ Given the pipe map, current coordinate and travel direction, return the next step of
    walking the network as a PipeWalkInfo instance. """

    x, y = current_coord

    # Given the current coordinate and travel direction, figure out what the next coordinate is.
    next_coord = {
        TravelDirection.UP:    (x, y-1),
        TravelDirection.DOWN:  (x, y+1),
        TravelDirection.LEFT:  (x-1, y),
        TravelDirection.RIGHT: (x+1, y),
    }[travel_direction]
    
    # If the next cell is out of bounds, or is a space character, this means we've reached the end
    # of our walk, so let's return a PipeWalkInfo indicating we're done.
    try:
        cell = map[next_coord]
        if cell == ' ':
            raise ValueError()
    except (KeyError, ValueError):
        return PipeWalkInfo(None, None, None, 0)
        
    # So long as the next cell isn't a junction, return a PipeWalkInfo indicating this next step
    # along the way.
    if cell != JUNCTION_PIPE:
        return PipeWalkInfo(value=cell, coord=next_coord, travel_direction=travel_direction, step_size=1)

    # If the next step is a junction, let's just continue straight through the junction.
    nx, ny = next_coord
    neighbors_of_junction = [
        (TravelDirection.UP,    (nx, ny-1)),
        (TravelDirection.DOWN,  (nx, ny+1)),
        (TravelDirection.LEFT,  (nx-1, ny)),
        (TravelDirection.RIGHT, (nx+1, ny))
    ]

    for new_dir, junction_exit in neighbors_of_junction:

        # Don't go back the way we came
        if junction_exit == current_coord:
            continue
        
        # Try this neighbor -- if we go out of bounds or it's a space character, this
        # is not the exit from the junction.
        try:
            jcell = map[junction_exit]
            if jcell == ' ':
                raise ValueError()
        except (KeyError, ValueError):
            continue
        
        # We've found the junction exit, return a PipeWalkInfo indicating the step after exiting
        # the junction, with a step size of 2 because we stepped into the junction and then out of
        # it all at once.
        return PipeWalkInfo(value=jcell, coord=junction_exit, travel_direction=new_dir, step_size=2)


@aoc_output_formatter(2017, 19, 1, 'letters seen in order')
def part_one(map, current_coord):
    
    # Start off traveling down, at the first vertical pipe leading into the map
    current_cell = VERTICAL_PIPE
    travel_direction = TravelDirection.DOWN

    visited_letter_sequence = list()
    
    # Walk through the pipes until we reach the exit
    while current_cell is not None:
        pipe_walk_info = _get_next_pipewalkinfo(current_coord, map, travel_direction)
        
        current_cell = pipe_walk_info.value
        travel_direction = pipe_walk_info.travel_direction
        current_coord = pipe_walk_info.coord

        if current_cell in LETTERS:
            visited_letter_sequence.append(current_cell)
            
    return ''.join(visited_letter_sequence)


@aoc_output_formatter(2017, 19, 2, 'steps taken to navigate the network')
def part_two(map, current_coord):
    
    # Start off traveling down, at the first vertical pipe leading into the map
    current_cell = VERTICAL_PIPE
    travel_direction = TravelDirection.DOWN
    
    distance = 1
    
    # Walk through the pipes until we reach the exit
    while current_cell is not None:
        pipe_walk_info = _get_next_pipewalkinfo(current_coord, map, travel_direction)
        
        current_cell = pipe_walk_info.value
        travel_direction = pipe_walk_info.travel_direction
        current_coord = pipe_walk_info.coord
        
        distance += pipe_walk_info.step_size
    
    return distance

#---------------------------------------------------------------------------------------------------

def run(input_file):

    map = get_input(input_file)

    # Find the starting coordinate which is the top row of the map where the vertical pipe is.
    for x, space in enumerate(map[0]):
        if space == VERTICAL_PIPE:
            current_coord = (x, 0)
            break
    
    # Turn the map array of strings into a dictionary of the value at each cell, for easier nav.
    map_dict = dict()
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            map_dict[(x, y)] = cell

    part_one(map_dict, current_coord)
    part_two(map_dict, current_coord)

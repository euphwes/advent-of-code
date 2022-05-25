from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable, int_stream, bidirectional_range
from util.structures import get_neighbors_of

#---------------------------------------------------------------------------------------------------

def _evaluate_octopi_energy_step(octopi_energy):
    """ Evaluates the octopi energy for each octopus in the grid, at the next time step. All octopus
    energy increases by 1 at each time step, and when the energy exceeds 9 the octopus flashes and
    its energy drops to zero. All octopi which are adjacent to a flashing octopus have their energy
    incremented by an additional 1.

    Returns the octopi_energy grid at the next time step, as well as a set of coordinates of all
    octopi which flashed during this evaluation. """

    # Store a dict of (x,y) coordinate and the energy value the octopus at that coord will have next
    next_step_energy_map = dict()

    # Take a first pass through the grid and store the current energy + 1 for each octopus
    for y in range(len(octopi_energy)):
        for x in range(len(octopi_energy[0])):
            octopi_energy[y][x] += 1
            next_step_energy_map[(x, y)] = octopi_energy[y][x]

    # Store which octopi (coords) have flashed this step.
    flashes_this_step = set()

    # Find which octopi should flash (energy > 9) and store those in the set of "flashed octopi".
    # For each octopus which flashes, add 1 energy to all adjacent octopi.
    # Keep passing through the energy list to find new octopi which might flash (due to adjacent
    # flashes) until no new flashing octopi are found.
    while True:
        any_flashes_this_pass = False
        for p, val in next_step_energy_map.items():
            x, y = p
            if val > 9 and (x, y) not in flashes_this_step:
                any_flashes_this_pass = True
                flashes_this_step.add((x, y))
                for _, n in get_neighbors_of(x, y, octopi_energy, include_diagonals=True, with_coords=True):
                    nx, ny = n
                    next_step_energy_map[(nx, ny)] += 1
                break
        if not any_flashes_this_pass:
            break

    # Any octopi which flashed this step have 0 energy next.
    for x, y in flashes_this_step:
        next_step_energy_map[(x, y)] = 0

    # Stick the "energy next step" back into the octopus grid.
    for p, val in next_step_energy_map.items():
        x, y = p
        octopi_energy[y][x] = val

    return octopi_energy, flashes_this_step



@aoc_output_formatter(2021, 11, 1, 'total flashes after 100 steps')
def part_one(octopi_energy):
    flash_count = 0
    for _ in range(100):
        octopi_energy, flashes_this_step = _evaluate_octopi_energy_step(octopi_energy)
        flash_count += len(flashes_this_step)

    return flash_count


@aoc_output_formatter(2021, 11, 2, 'first step where all octopi flash')
def part_two(octopi_energy):
    for step_num in int_stream():
        octopi_energy, flashes_this_step = _evaluate_octopi_energy_step(octopi_energy)
        if len(flashes_this_step) == 100:
            return step_num + 1

#---------------------------------------------------------------------------------------------------

def run(input_file):

    def _get_starting_values():
        lines = [line for line in get_input(input_file)]

        values = list()
        for line in lines:
            line = list(line)
            values.append([int(x) for x in line])

        return values

    part_one(_get_starting_values())
    part_two(_get_starting_values())

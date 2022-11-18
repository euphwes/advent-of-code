from util.decorators import aoc_output_formatter
from util.input import get_input
from .common_2017 import knot_hash, build_dense_hex_hash

#---------------------------------------------------------------------------------------------------

CELL_USED = '1'

def _find_used_square_not_in_region(disk_map):
    """ Iterate the map and find any used square which is not yet marked as part of a region.
    Used squares already found to be in a region will be marked with their region number. """

    for coord, value in disk_map.items():
        if value == CELL_USED:
            return coord

    return None


def _get_used_neighbors_of(target, disk_map):
    """ Check all adjacent neighbors of the target coordinate, and return a list of those neighbors
    which are used squares. """

    used_neighbors = list()

    x, y = target
    for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        try:
            ncell = disk_map[(nx, ny)]
            if ncell == CELL_USED:
                used_neighbors.append((nx, ny))
        except KeyError:
            pass

    return used_neighbors


def _get_all_coords_in_region(start_coord, disk_map):
    """ Given a starting coordinate, return the coordinates of all used squares which form a region
    with this coordinate because they are directly or indirectly adjacent. """

    cells_in_region = set()

    queue = [start_coord]
    while queue:
        curr_coord = queue.pop(0)
        cells_in_region.add(curr_coord)

        for neighbor in _get_used_neighbors_of(curr_coord, disk_map):
            if neighbor not in cells_in_region:
                queue.append(neighbor)

    return cells_in_region


def _build_disk_from_knot_hashes(key):
    """ Build and return a grid representing a storage disk, where the the state of the disk is
    defined by the (day 10) Knot Hash a key value for each row in the disk. """

    disk_map = dict()

    # There are 128 rows in the disk, and the index of the row is the y value in the (x, y) grid.
    for y in range(128):

        # Turn the row-specific key into a list of integers/bytes for the hash appended with the
        # special knot has magic integers.
        input_bytes = [ord(c) for c in f'{key}-{y}'] + [17, 31, 73, 47, 23]

        # Run the hash and get the hex representation
        sparse_hash = knot_hash(input_bytes, iterations=64)
        dense_hex_hash = build_dense_hex_hash(sparse_hash)

        # Turn the hex representation into a binary string where each hex digit is replaced by its
        # 4-digit binary representation.
        bin_hash = ''.join([bin(int(char, base=16))[2:].zfill(4) for char in dense_hex_hash])

        # Store the value of each cell in the disk into its (x,y) coord in the disk.
        for x, cell_value in enumerate(bin_hash):
            disk_map[(x, y)] = cell_value

    return disk_map


@aoc_output_formatter(2017, 14, 1, 'number of used squares in the grid')
def part_one(key):
    disk_map = _build_disk_from_knot_hashes(key)
    return sum(1 for cell in disk_map.values() if cell == CELL_USED)


@aoc_output_formatter(2017, 14, 2, 'number of regions comprised of adjacent used squares')
def part_two(key):
    disk_map = _build_disk_from_knot_hashes(key)

    curr_region_num = 0
    while True:
        unregioned_coord = _find_used_square_not_in_region(disk_map)
        if unregioned_coord is None:
            break

        curr_region_num += 1

        coords_in_region = _get_all_coords_in_region(unregioned_coord, disk_map)
        for coord in coords_in_region:
            disk_map[coord] = curr_region_num

    return curr_region_num

#---------------------------------------------------------------------------------------------------

def run(input_file):

    key = get_input(input_file)[0]

    part_one(key)
    part_two(key)

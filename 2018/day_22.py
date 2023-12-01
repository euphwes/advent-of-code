from enum import Enum, auto
from functools import lru_cache
from heapq import heappop, heappush, heapify

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable, triple_iterable


DAY = 22
YEAR = 2018

PART_ONE_DESCRIPTION = "total risk level of smallest box including start and target"
PART_ONE_ANSWER = 8681

PART_TWO_DESCRIPTION = "minutes elapsed during shortest path to the target"
PART_TWO_ANSWER = 1070


class Tool(Enum):
    TORCH = 0
    NEITHER = 1
    CLIMBING_GEAR = 2


class RegionType(Enum):
    WET = auto()
    ROCKY = auto()
    NARROW = auto()


EROSION_MODULO_REGIONTYPE_MAP = {
    0: RegionType.ROCKY,
    1: RegionType.WET,
    2: RegionType.NARROW,
}

REGIONTYPE_RISK_VALUE_MAP = {v: k for k, v in EROSION_MODULO_REGIONTYPE_MAP.items()}


@lru_cache(maxsize=None)
def _erosion_level(x, y, depth, target):
    geologic_index = _geologic_index(x, y, depth, target)
    return (geologic_index + depth) % 20183


@lru_cache(maxsize=None)
def _geologic_index(x, y, depth, target):
    if (x, y) in {(0, 0), target}:
        return 0

    if y == 0:
        return x * 16807

    if x == 0:
        return y * 48271

    else:
        n1_erosion = _erosion_level(x - 1, y, depth, target)
        n2_erosion = _erosion_level(x, y - 1, depth, target)
        return n1_erosion * n2_erosion


def _region_type(x, y, depth, target) -> RegionType:
    erosion_level = _erosion_level(x, y, depth, target)
    return EROSION_MODULO_REGIONTYPE_MAP[erosion_level % 3]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(depth, target_coord):
    risk_level = 0
    for x in range(target_coord[0] + 1):
        for y in range(target_coord[1] + 1):
            risk_level += REGIONTYPE_RISK_VALUE_MAP[
                _region_type(x, y, depth, target_coord)
            ]

    return risk_level


VALID_TOOLS_BY_REGIONTYPE = {
    RegionType.WET: {Tool.CLIMBING_GEAR, Tool.NEITHER},
    RegionType.ROCKY: {Tool.TORCH, Tool.CLIMBING_GEAR},
    RegionType.NARROW: {Tool.NEITHER, Tool.TORCH},
}


def _all_3d_neighbors(x, y, z):
    yield from [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, 0),
        (x, y, 1),
        (x, y, 2),
    ]


def _is_3d_coord_valid(x, y, z, regiontype_map):
    if (x, y) not in regiontype_map:
        return False

    region_type = regiontype_map[(x, y)]
    tool = Tool(z)
    return tool in VALID_TOOLS_BY_REGIONTYPE[region_type]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(depth, target_coord):
    regiontype_map = dict()

    x_bound = 50
    y_bound = 790

    # Precalculate the region type for all regions in a rectangle bounding the target,
    # hopefully large enough to encapsulate the best path.
    for x, y in nested_iterable(range(x_bound), range(y_bound)):
        regiontype_map[(x, y)] = _region_type(x, y, depth, target_coord)

    # Consider the "tool" to be an added 3rd dimension with Z values only 0, 1, and 2.
    # Torch is Z=0, Neither is Z=1, Climbing Gear is Z=2.
    # Find the edge weights between all adjacent cells in the 3D space between (0, 0, 0)
    # and (TARGET_X, TARGET_Y, 3).
    # The edge weight is 1 if you can travel between those cells without a tool change, and
    # it's 8 if you need a tool change (7 to change tools, then 1 to travel).
    cell_edge_weights = dict()

    for x, y, z in triple_iterable(range(x_bound), range(y_bound), range(3)):
        if not _is_3d_coord_valid(x, y, z, regiontype_map):
            continue

        cell_edge_weights[(x, y, z)] = set()

        for nx, ny, nz in _all_3d_neighbors(x, y, z):
            if not _is_3d_coord_valid(nx, ny, nz, regiontype_map):
                continue
            if (x, y, z) == (nx, ny, nz):
                continue

            # If (x, y) is the same and z is different, that's changing a tool.
            # For a given (x, y), only 2 tools are valid, so we won't have a cell at the
            # unsupported tool's z.
            if (x, y) == (nx, ny):
                cell_edge_weights[(x, y, z)].add(((nx, ny, nz), 7))
                continue

            if z == nz:
                cell_edge_weights[(x, y, z)].add(((nx, ny, nz), 1))
                continue

    visited = set()
    queue = [(0, (0, 0, 0))]

    tx, ty = target_coord
    tz = Tool.TORCH.value

    while queue:
        minutes_so_far, coord = heappop(queue)
        visited.add(coord)

        queue = [t for t in queue if t[1] not in visited]
        heapify(queue)

        for neighbor, min_to_neighbor in cell_edge_weights[coord]:
            if neighbor == (tx, ty, tz):
                return minutes_so_far + min_to_neighbor
            if neighbor not in visited:
                heappush(queue, (minutes_so_far + min_to_neighbor, neighbor))


# ----------------------------------------------------------------------------------------------


def run(input_file):
    cave_info = get_input(input_file)

    depth = int(cave_info[0].replace("depth: ", ""))
    raw_target = [int(n) for n in cave_info[1].replace("target: ", "").split(",")]
    target_coord = int(raw_target[0]), int(raw_target[1])

    # Sample
    # depth = 510
    # target_coord = (10, 10)

    part_one(depth, target_coord)
    part_two(depth, target_coord)

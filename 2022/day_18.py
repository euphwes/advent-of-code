from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 18
YEAR = 2022

PART_ONE_DESCRIPTION = "total surface area of lava cubes"
PART_ONE_ANSWER = 4242

PART_TWO_DESCRIPTION = "external surface area of lava cubes"
PART_TWO_ANSWER = 2428


def _neighbor_coords(x, y, z):
    """Yield all the coordinates immediately adjacent (no diagonals) to the provided coord."""

    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


def _get_lava_cubes(lava_coords):
    """Parse the problem input and return a set of 3D coordinates which represent lava cubes."""

    lava_cubes = set()
    for line in lava_coords:
        x, y, z = (int(n) for n in line.split(","))
        lava_cubes.add((x, y, z))

    return lava_cubes


def _has_path_to_outside(cube_coord, lava_cubes, max_x, max_y, max_z):
    """Returns if a given coordinate has a path to the outside by using 3D BFS."""

    def _is_outside(test):
        x, y, z = test
        return any(
            [
                x < 0,
                y < 0,
                z < 0,
                x > max_x,
                y > max_y,
                z > max_z,
            ]
        )

    visited = set()
    queue = list()
    queue.append(cube_coord)

    while queue:
        test_me = queue.pop(0)
        if _is_outside(test_me):
            return True

        x, y, z = test_me
        for neighbor in _neighbor_coords(x, y, z):
            if neighbor in lava_cubes:
                continue
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False


def _get_trapped_air_cubes(lava_cubes):
    """Return a set of all "trapped air cubes" coordinates, which are cubes of air surrounded by
    lava in such a way that there is no way to access that air from the outisde."""

    # Rather than checking ALL air inside the box bounded by the lava cubes extremeties, we can
    # just check the air cubes which are immediately adjacent to a lava cube.
    air_to_check = set()
    for x, y, z in lava_cubes:
        for neighbor in _neighbor_coords(x, y, z):
            if neighbor not in lava_cubes:
                air_to_check.add(neighbor)

    # We use 0 and max_(x,y,z) to define the limits of the area bounded by the lava cubes.
    # A cube is "outside" if is at or outside any of these boundaries.
    max_x = max(x for x, _, _ in lava_cubes)
    max_y = max(y for _, y, _ in lava_cubes)
    max_z = max(z for _, _, z in lava_cubes)

    return set(
        cube
        for cube in air_to_check
        if not _has_path_to_outside(
            cube,
            lava_cubes,
            max_x,
            max_y,
            max_z,
        )
    )


def _get_surface_area(lava_cubes, disqualifying_cubes):
    """Returns the surface area of all given lava cubes. Assuming 6 units of surface area per
    cube (1 per side), but reduced by any adjacent disqualifying cube. For example, a lava cube
    next to another lava cube does not have surface area exposed on the shared face. Nor does a
    lava cube adjacent to a trapped internal air pocket (if we include that)."""

    exposed_surface_area = 0

    for x, y, z in lava_cubes:
        local_area = 6
        for neighbor in _neighbor_coords(x, y, z):
            if neighbor in disqualifying_cubes:
                local_area -= 1
        exposed_surface_area += local_area

    return exposed_surface_area


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(lava_coords):

    lava_cubes = _get_lava_cubes(lava_coords)

    return _get_surface_area(lava_cubes, lava_cubes)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(lava_coords):

    lava_cubes = _get_lava_cubes(lava_coords)

    # Only counting "exposed" surface area, so we're not counting lava adjacent to
    # internally-trapped air pockets as having that side be exposed surface area.
    disqualifying_cubes = lava_cubes | _get_trapped_air_cubes(lava_cubes)

    return _get_surface_area(lava_cubes, disqualifying_cubes)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    lava_coords = get_input(input_file)

    part_one(lava_coords)
    part_two(lava_coords)

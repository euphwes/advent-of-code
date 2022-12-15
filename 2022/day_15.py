from util.algs import manhattan_distance as distance
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 15
YEAR = 2022

PART_ONE_DESCRIPTION = "number of cells in row y=2000000 that can't contain a beacon"
PART_ONE_ANSWER = 5525847

PART_TWO_DESCRIPTION = "tuning frequency of the distress beacon"
PART_TWO_ANSWER = 13340867187704


def _parse_sensor_info(stuff):
    """Parse the problem input to return three things: a set of all sensor coordinates, a set
    of beacon coordinates, and a map of sensor to "beacon-free zone" distance within which a
    beacon can't exist because that would be closer than the closest beacon."""

    sensors_to_nearest_beacon = dict()
    sensor_beacon_free_zones = dict()

    # Start by parsing the raw lines and mapping each sensor to its nearest beacon
    for line in stuff:
        raw_sensor, raw_beacon = line.split(": ")

        # Extract the x,y coords of the sensor
        raw_sensor = raw_sensor.replace("Sensor at ", "")
        raw_sx, raw_sy = raw_sensor.split(", ")
        sx = int(raw_sx.replace("x=", ""))
        sy = int(raw_sy.replace("y=", ""))

        # Extract the x,y coords of the beacon
        raw_beacon = raw_beacon.replace("closest beacon is at ", "")
        raw_bx, raw_by = raw_beacon.split(", ")
        bx = int(raw_bx.replace("x=", ""))
        by = int(raw_by.replace("y=", ""))

        sensors_to_nearest_beacon[(sx, sy)] = (bx, by)

    # Extract sets of all sensors and beacons
    sensors = set(sensors_to_nearest_beacon.keys())
    beacons = set(sensors_to_nearest_beacon.values())

    # For each sensor, figure out the Manhattan distance to its nearest beacon. Within this
    # area, other beacons cannot exist (becauase they'd be as close as, or closer than, the
    # actual nearest beacon to this sensor).
    for sensor in sensors:
        nearest_beacon = sensors_to_nearest_beacon[sensor]
        sensor_beacon_free_zones[sensor] = distance(sensor, nearest_beacon)

    return sensors, beacons, sensor_beacon_free_zones


def _is_beacon_impossible(target, beacon_free_zones, beacons):
    """Given a target coordinate, returns True if it's impossible for a beacon to be at that
    position (because it would be within a sensor's beacon-free zone)."""

    if target in beacons:
        return False

    for sensor, threshold_distance in beacon_free_zones.items():
        if distance(target, sensor) <= threshold_distance:
            return True

    return False


def _sensor_perimeter_coordinates(sensor, distance):
    """A generator which yields all coordinates along the "perimeter" of a boundary defined by
    a given central coordinate, and a Manhattan distance away from that coordinate."""

    sensor_x, sensor_y = sensor

    # Start immediately right of the sensor, `distance` units away.
    y = sensor_y
    x = sensor_x + distance

    # Move diagonally up and left until we are directly above the sensor (still `distance` units
    # away), yielding every coordinate along the way.
    while x > sensor_x:
        yield (x, y)
        x -= 1
        y -= 1

    yield (x, y)

    # Move diagonally down and left until we are directly to the left of the sensor (still
    # `distance` units away), yielding every coordinate along the way.
    while y < sensor_y:
        yield (x, y)
        x -= 1
        y += 1

    yield (x, y)

    # Move diagonally down and right until we are directly below the sensor (still `distance`
    # units away), yielding every coordinate along the way.
    while x < sensor_x:
        yield (x, y)
        x += 1
        y += 1

    yield (x, y)

    # Move diagonally up and right until we are directly to the right the sensor (still
    # `distance` units away), yielding every coordinate along the way.
    while y > sensor_y:
        yield (x, y)
        x += 1
        y -= 1

    yield (x, y)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(problem_input):

    sensors, beacons, beacon_free_zones = _parse_sensor_info(problem_input)

    # For all "beacon free zones" find the one with the largest size
    dx = max(beacon_free_zones.values())

    # Find the min and max x coordinates across all sensors, and extend that by the largest
    # beacon free zone size found above. This should give us the maximum x coord window we need
    # to check to be sure that no beacons reside in it.
    min_x = min(s[0] for s in sensors) - dx
    max_x = max(s[0] for s in sensors) + dx

    # For every possible x value in the row y=2000000, count how many cells in that row could
    # not contain a beacon.
    count = 0
    for x in range(min_x, max_x):
        if _is_beacon_impossible((x, 2000000), beacon_free_zones, beacons):
            count += 1
    return count


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(problem_input):

    _, beacons, beacon_free_zones = _parse_sensor_info(problem_input)

    # Given that the problem tells us there's only a single coordinate (within our reduced
    # search area) that the distress beacon can possibly reside, we know that it must lie
    # somewhere 1 cell outside of the perimeter around a sensor defined by its beacon-free zone.
    #
    # For every sensor, iterate over all coordinates that define the perimeter around that
    # sensor where a beacon *might* be, because it's just outside that sensor's beacon-free
    # zone. Then, check if it's impossible to have a beacon there -- that point might reside
    # within another sensor's beacon-free zone.
    #
    # Once we find a coordinate where it's *not* impossible for a beacon to be, we know that
    # must be the location of the distress beacon.

    for sensor, no_beacon_distance in beacon_free_zones.items():
        for tx, ty in _sensor_perimeter_coordinates(sensor, no_beacon_distance + 1):

            # Part 2 reduces the search space, we know the beacon is in a region defined by
            # 0 <= x <= 4_000_000
            # 0 <= y <= 4_000_000
            if not (tx >= 0 and tx <= 4_000_000 and ty >= 0 and ty <= 4_000_000):
                continue

            if not _is_beacon_impossible((tx, ty), beacon_free_zones, beacons):
                return tx * 4_000_000 + ty


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

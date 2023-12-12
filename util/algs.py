def manhattan_distance(coord1, coord2):
    """Returns the Manhattan distance between two coordinates."""

    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1 - x2) + abs(y1 - y2)


def manhattan_distance_3d(coord1, coord2):
    """Returns the Manhattan distance between two 3D coordinates."""

    x1, y1, z1 = coord1
    x2, y2, z2 = coord2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def manhattan_distance_4d(coord1, coord2):
    """Returns the Manhattan distance between two 4D coordinates."""

    x1, y1, z1, t1 = coord1
    x2, y2, z2, t2 = coord2

    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) + abs(t1 - t2)

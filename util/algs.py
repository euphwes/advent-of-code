def manhattan_distance(coord1, coord2):
    """ Returns the Manhattan distance between two coordinates. """

    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1-x2) + abs(y1-y2)

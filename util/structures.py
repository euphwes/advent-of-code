""" A module that provides functions for working with common data structures. """

from util.iter import nested_iterable

def get_neighbors_of(pos_x, pos_y, grid, include_diagonals=True, with_coords=False):
    """ Returns a generator which yields all of neighbors of a particular position in a grid.
    Neighbors include all directly adjacent cells, as well as diagonals unless `include_diagonals`
    is False. If `with_coords` is True, this yields `(neighbor, (x,y) coords of neighbor)`. """

    max_x = len(grid[0])
    max_y = len(grid)

    neighboring_x = [x for x in [pos_x-1, pos_x, pos_x+1] if x >= 0 and x < max_x]
    neighboring_y = [y for y in [pos_y-1, pos_y, pos_y+1] if y >= 0 and y < max_y]

    for x, y in nested_iterable(neighboring_x, neighboring_y):
        # This isn't a neighbor, this is the cell itself. Skip it.
        if (x, y) == (pos_x, pos_y):
            continue

        # This is a diagonal, only include it if the caller requested diagonals.
        if (x != pos_x) and (y != pos_y) and not include_diagonals:
            continue

        if not with_coords:
            yield grid[y][x]
        else:
            yield grid[y][x], (x, y)

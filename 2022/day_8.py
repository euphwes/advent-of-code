from util.decorators import aoc_output_formatter
from util.input import get_input_grid_map

DAY = 8
YEAR = 2022

PART_ONE_DESCRIPTION = "number of trees visible outside the grid"
PART_ONE_ANSWER = 1543

PART_TWO_DESCRIPTION = "maximum scenic score of a tree"
PART_TWO_ANSWER = 595080


def _is_visible(tree_coordinate, forest, forest_width, forest_height):
    """Returns whether the tree at the specified coordinate is visible from outside the
    forest."""

    tree = forest[tree_coordinate]
    cx, cy = tree_coordinate

    # If the tree is on a border, it's visible.
    if cx in (0, forest_width - 1) or cy in (0, forest_height - 1):
        return True

    # Check from each of the edges into the target tree to see if it's visible.
    visible_up = not any(forest[(cx, y)] >= tree for y in range(0, cy))
    visible_down = not any(
        forest[(cx, y)] >= tree for y in range(cy + 1, forest_height)
    )
    visible_left = not any(forest[(x, cy)] >= tree for x in range(0, cx))
    visible_right = not any(
        forest[(x, cy)] >= tree for x in range(cx + 1, forest_width)
    )

    # The tree is visible from outside the forest if it's visible from any edge.
    return any((visible_down, visible_up, visible_right, visible_left))


def _scenic_score(tree_coordinate, forest, forest_width, forest_height):
    """Calculates the "scenic score" of a tree at the specified coordinate, where the score is
    the product of the number of consecutive adjacent trees in each direction until you reach
    a neighboring tree of the same height or higher."""

    tree = forest[tree_coordinate]
    cx, cy = tree_coordinate

    # If the tree is on a border, its score is 0.
    if cx in (0, forest_width - 1) or cy in (0, forest_height - 1):
        return 0

    # Start a score for each cardinal direction, and the score for each direction is the number
    # of trees you find as you walk away from the target tree whose height is less than the
    # target tree. Include a point for the final (as tall or taller) tree you find.

    left_score = 0
    for x in reversed(range(0, cx)):
        left_score += 1
        if forest[(x, cy)] >= tree:
            break

    right_score = 0
    for x in range(cx + 1, forest_width):
        right_score += 1
        if forest[(x, cy)] >= tree:
            break

    up_score = 0
    for y in reversed(range(0, cy)):
        up_score += 1
        if forest[(cx, y)] >= tree:
            break

    down_score = 0
    for y in range(cy + 1, forest_height):
        down_score += 1
        if forest[(cx, y)] >= tree:
            break

    return down_score * up_score * right_score * left_score


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(forest):

    width = max([x for x, y in forest.keys()]) + 1
    height = max([y for x, y in forest.keys()]) + 1

    return sum(
        1 for coord in forest.keys() if _is_visible(coord, forest, width, height)
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(forest):

    width = max([x for x, y in forest.keys()]) + 1
    height = max([y for x, y in forest.keys()]) + 1

    return max(_scenic_score(coord, forest, width, height) for coord in forest.keys())


# ----------------------------------------------------------------------------------------------


def run(input_file):

    forest = get_input_grid_map(input_file)
    forest = {coord: int(tree) for coord, tree in forest.items()}

    part_one(forest)
    part_two(forest)

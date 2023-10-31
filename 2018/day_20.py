from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 20
YEAR = 2018

PART_ONE_DESCRIPTION = "Largest number of doors required to reach a room"
PART_ONE_ANSWER = 3014

PART_TWO_DESCRIPTION = "Number of rooms a least 1000 doors away"
PART_TWO_ANSWER = 8279


def _get_ix_of_closing_paren(subroute):
    """For a substring of a route which starts with a parentheses, return the index of the
    matching closing parentheses.

    Eg: (EESS) --> 5
             *

    Eg: (EE(SE|NE))SS(EE) --> 10
                  *
    """
    open_parens = list()

    for i, char in enumerate(subroute):
        if char == "(":
            open_parens.append(i)
        elif char == ")":
            open_parens.pop()
            if not open_parens:
                return i


def _follow_map_and_get_location_to_steps_map(route_regex):
    # Trim the framing ^ and $
    route_regex = route_regex[1:-1]

    # Store (x, y) coordinates and the amount of steps taken to get there
    location_steps = dict()

    # Store current (x, y) coord, number of steps so far, and the path currently being followed
    branches_to_follow = list()
    branches_to_follow.append((0, 0, 0, route_regex))

    # While there are still paths to walk in this branch...
    while branches_to_follow:
        curr_x, curr_y, curr_steps, branch = branches_to_follow.pop(0)
        branch = list(branch)

        # While we can just follow the corridor without worrying about branches...
        while branch and branch[0] != "(":
            # Follow the next step in the right direction and record the total number of steps
            # it takes to get to that (x,y) coord.
            step = branch.pop(0)

            curr_steps += 1
            if step == "E":
                curr_x += 1
            elif step == "W":
                curr_x -= 1
            elif step == "N":
                curr_y += 1
            elif step == "S":
                curr_y -= 1
            else:
                raise ValueError(f"Oops, don't know what to do with {step}")

            # If we haven't already been to this location, record the total number of steps to
            # get here. If we've already seen it, don't record anything, because we care about
            # the shortest path to get to each location.
            if (curr_x, curr_y) not in location_steps:
                location_steps[(curr_x, curr_y)] = curr_steps

        # If we've walked all the way down this branch and there's nowhere left to walk,
        # go and following the next branch on the queue.
        if not branch:
            continue

        # We've reached a branch -- find the parenthesed-enclosed portion which indicates
        # the route options we have to take at this junction.
        closing_ix = _get_ix_of_closing_paren(branch)
        raw_branch_options = "".join(branch[1:closing_ix])

        # Sometimes we can continue straight from here, instead of following a branch.
        # If there's anything left after the parens-enclosed branch, remember it.
        found_stuff_after_options = None
        if closing_ix and branch[closing_ix + 1 :]:
            found_stuff_after_options = "".join(branch[closing_ix + 1 :])

        # Parse the paren-enclosed branch at the pipes, but only the ones inside the outermost
        # level of parentheses
        #
        # Eg:  (NNN|SSS|EE(SS|NN))
        #
        # is parsed as the following 3 branches from this point:
        #     1. NNN
        #     2. SSS
        #     3. EE(SS|NN)
        branch_options = list()
        open_parens_stack = list()
        new_option = ""

        for char in raw_branch_options:
            if char == "(":
                new_option += char
                open_parens_stack.append("x")
            elif char == ")":
                new_option += char
                open_parens_stack.pop()
            elif char == "|":
                if not open_parens_stack:
                    branch_options.append(new_option)
                    new_option = ""
                else:
                    new_option += char
            else:
                new_option += char

        # We might still be in the middle of recording the last branch option if we're done with
        # the loop.
        if new_option:
            branch_options.append(new_option)

        # If we had the option to continue straight instead of following a branch, just consider
        # that a branch too.
        #
        # Eg: (NN|SS)EEES
        #
        # We'd parse NN and SS out of the branches, but then you can also go EEES so let's
        # just consider that a branch, too.
        if found_stuff_after_options:
            branch_options.append(found_stuff_after_options)

        # For each branch available to us, put that on the queue with our current coordinate and
        # steps taken so we can explore those branches later.
        for option in branch_options:
            branches_to_follow.append((curr_x, curr_y, curr_steps, option))

    return location_steps


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(route_regex):
    location_steps = _follow_map_and_get_location_to_steps_map(route_regex)
    return max(location_steps.values())


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(route_regex):
    location_steps = _follow_map_and_get_location_to_steps_map(route_regex)

    count_far_away = 0
    for steps in location_steps.values():
        if steps >= 1000:
            count_far_away += 1

    return count_far_away


# ----------------------------------------------------------------------------------------------


def run(input_file):
    route_regex = get_input(input_file)[0]

    part_one(route_regex)
    part_two(route_regex)

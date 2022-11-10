from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import Counter

# Important note to whoever is reading this: I recognize this is fundamentally a "tree problem",
# but at the moment I decided I simply didn't feel like building and traversing a tree. So I did it
# in this terrible, awful, no good, very bad way.

# BUT, as popular wisdom tells us -- "it's not stupid if it works."

#---------------------------------------------------------------------------------------------------

# Global variables, maps of program names to their weights, and sets of their children's names.
# I decided to make these globals because it was getting tedious to pass them around between lots
# of helper functions.
weights_dict = None
children_dict = None


def _parse_tree(tree_description):
    """ Parses the problem input (a description of the tree/tower of stacked programs), building
    maps of program name to their weight, and program name to a set of their children programs.

    Ex:
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    """

    global weights_dict, children_dict
    weights_dict = dict()
    children_dict = dict()

    for line in tree_description:
        first_split = line.split(' -> ')
        if len(first_split) == 1:
            children = set()
        else:
            children = set(first_split[1].split(', '))
        name, weight_with_parens = first_split[0].split(' ')
        weight = int(weight_with_parens[1:-1])

        weights_dict[name] = weight
        children_dict[name] = children


def _find_root_program():
    """ Finds the bottom program in the tower by identifying the program which isn't the child of
    any other programs. """

    # Find programs that have children, because the root must be one of those. We can disregard
    # "leaf nodes", aka programs at the top of the tower with no children of their own.
    programs_with_children = [name for name, children in children_dict.items() if children]

    # For each candidate program...
    for name in programs_with_children:

        # Start by assuming it's not the child of another.
        is_a_child = False

        # Check all other programs which have children, and if the candidate program is a child of
        # any other parent, it's not the root.
        for parent in [n for n in programs_with_children if n != name]:
            if name in children_dict[parent]:
                is_a_child = True
                break

        # If the candidate program is not a child of any other parent, it's the root program
        if not is_a_child:
            return name


def _get_tower_weight(tower_root):
    """ Calculates the weight of the tower of programs with the program named `tower_root` at
    the bottom. This is the sum of the root program's weight and all programs stacked above it. """

    weight = weights_dict[tower_root]
    for child in children_dict[tower_root]:
        weight += _get_tower_weight(child)

    return weight


def _find_correct_weight_for_misweighted_program(current_program):
    """ Starting at the root of the program tower, traverses the tree to find the program which does
    not have the correct weight, and then calculates and returns the correct weight which would
    balance the tree. """

    # Holds the weights of each sub-tower as we calculate them
    tower_weights = {current_program: _get_tower_weight(current_program)}

    while True:
        # For each child of the current program, calculate and store the child's tower's weight
        # in the dictionary for future reference, and also store it in a list of the weights of just
        # the current children.
        local_children_weights = []
        for child in children_dict[current_program]:
            child_tower_weight = _get_tower_weight(child)
            tower_weights[child] = child_tower_weight
            local_children_weights.append(child_tower_weight)

        proceed_to_next_level = False
        proceed_to_weight_adjustment_calc = False

        # Count the number of occurences of each weight
        for weight, count in Counter(local_children_weights).items():

            # If any child tower weight occurs only once, that's a sub-tower with incorrect weight.
            # Take the current program as the "parent", set that child as the current program,
            # and set the flag to so we now check the weight of the next level of children.
            if count == 1:
                for child in children_dict[current_program]:
                    if tower_weights[child] == weight:
                        last_parent = current_program
                        current_program = child
                        proceed_to_next_level = True
                        break

            # If all the weights of the children are the same, the current program's sub-tower is
            # the one whose weight is wrong and needs to be adjusted. Set the flag to indicate we
            # no longer need to keep checking children, so we can move to the next step.
            elif count == len(local_children_weights):
                proceed_to_weight_adjustment_calc = True

        if proceed_to_next_level:
            continue
        if proceed_to_weight_adjustment_calc:
            break

    # The current program's tower weight is the one that's wrong. Get its weight, and the weights
    # of its siblings (aka the children of its parent).
    my_weight = tower_weights[current_program]
    weights_of_parents_children = [tower_weights[child] for child in children_dict[last_parent]]

    # The target tower weight is the one that occurs more than once (because this program's tower's
    # weight is the odd one out, indicating it's incorrect).
    for weight, count in Counter(weights_of_parents_children).items():
        if count > 1:
            tower_target_weight = weight
            break

    # Find the difference between this tower's weight and the target/correct weight from siblings.
    diff = abs(my_weight - tower_target_weight)

    # Because the children of this program are all balanced, the only way to adjust the tower weight
    # is to adjust the weight of this program itself by the difference found above.
    # This is the correct weight!
    return abs(diff - weights_dict[current_program])


@aoc_output_formatter(2017, 7, 1, 'name of the root program')
def part_one(tree_description):
    _parse_tree(tree_description)
    return _find_root_program()


@aoc_output_formatter(2017, 7, 2, 'correct weight of the program with incorrect weight')
def part_two(root_name):
    return _find_correct_weight_for_misweighted_program(root_name)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    tree_description = get_input(input_file)

    root_name = part_one(tree_description)
    part_two(root_name)

from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

class Bag:
    """ A tree node representing a colored bag, and the "children" nodes indicate bags this bag
    must contain. """

    def __init__(self, color, bag_rules):
        self.value = color
        self.children = list()

        for rule in bag_rules:
            if self.value == rule.color:
                for child_color_and_quantity in rule.held_colors_and_quantities:
                    for _ in range(child_color_and_quantity.quantity):
                        self.children.append(Bag(child_color_and_quantity.color, bag_rules))

    def count(self):
        """ Returns the number of children of this node, direct and indirect. """
        return len(self.children) + sum(child.count() for child in self.children)


class InverseBag:
    """ A tree node representing a colored bag, and the "children" nodes indicate a color of bag
    which can contain this bag. """

    def __init__(self, color, bag_rules):
        self.value = color
        self.children = list()

        for rule in bag_rules:
            if self.value in rule.held_colors:
                self.children.append(InverseBag(rule.color, bag_rules))


    def get_containing_colors(self):
        """ Returns the set of bag colors which directly or indirectly contain this bag color. """

        # The children of this bag color can contain this bag color directly
        colors = {child.value for child in self.children}

        # All the children of this bag's children can contain this bag color indirectly
        for child in self.children:
            colors.update(child.get_containing_colors())

        return colors


class BagColorAndQuantity:
    def __init__(self, color, quantity):
        self.color    = color
        self.quantity = quantity


class BagRule:
    """ Parses a line of the input to determine the specified bag color, and which bag colors and
    quantities of those bags it can hold. Returns a BagRule encapsulating this info. """

    def __init__(self, line):
        # ex: dark magenta bags contain 4 light indigo bags, 1 wavy lavender bag, 1 clear teal bag

        self.held_colors = list()
        self.held_colors_and_quantities = list()

        i = line.index('bags contain')
        self.color = line[:i].strip()
        held_bags_str  = line[i+12:]

        # If we see this color bag holds no others, held_colors_and_quantities is empty
        if 'no other' in held_bags_str:
            return

        # Otherwise, the remaining portion of the input line holds bag colors and qty
        for held_bag_component in held_bags_str.split(', '):
            pieces = held_bag_component.strip().split(' ')
            count = int(pieces[0])
            held_color = ' '.join([pieces[1].strip(), pieces[2].strip()])
            self.held_colors_and_quantities.append(BagColorAndQuantity(held_color, count))

        self.held_colors.extend(bcaq.color for bcaq in self.held_colors_and_quantities)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 7, 1, 'num colors which can hold shiny gold')
def part_one(input_lines):
    shiny_gold = InverseBag('shiny gold', [BagRule(line) for line in input_lines])
    return len(shiny_gold.get_containing_colors())


@aoc_output_formatter(2020, 7, 2, 'num bags which a shiny gold bag must hold')
def part_two(input_lines):
    shiny_gold = Bag('shiny gold', [BagRule(line) for line in input_lines])
    return shiny_gold.count()

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

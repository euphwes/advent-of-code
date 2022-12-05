from util.decorators import aoc_output_formatter
from util.input import get_input

from string import ascii_lowercase, ascii_uppercase

#---------------------------------------------------------------------------------------------------

def _get_priority(item):
    """ Returns the priority of the provided item. """
    if item in ascii_lowercase:
        # Lowercase characters have priority 1 through 26, their order in the alphabet.
        return ascii_lowercase.index(item) + 1
    else:
        # Uppercause characters have priority 27 through 52, their order in the alphabet + 26.
        return ascii_uppercase.index(item) + 27


@aoc_output_formatter(2022, 3, 1, 'combined priority of items shared between compartments', assert_answer=7889)
def part_one(rucksacks):

    total_priority = 0

    for sack in rucksacks:
        # Each rucksack has 2 compartments of equal size containing multiple items.
        # Split the sack in half to find each compartment.
        half = int(len(sack)/2)
        compartment_1, compartment_2 = sack[:half], sack[half:]
        
        # Find all the items in each compartment and then find the items which are
        # shared between both.
        compartment_1, compartment_2 = set(compartment_1), set(compartment_2)
        shared_items = compartment_1 & compartment_2
        
        # Sum the priorities of all shared items and add it to the running total
        total_priority += sum(_get_priority(item) for item in shared_items)
    
    return total_priority
                
        
@aoc_output_formatter(2022, 3, 2, 'combined priority of items shared between 3 grouped elves', assert_answer=2825)
def part_two(rucksacks):
    
    total_priority = 0
    
    # While we still have rucksacks left...
    while rucksacks:
        
        # Start off assuming all items are shared.
        shared_items = set(ascii_lowercase) | set(ascii_uppercase)
        
        # Then grab groups of 3 sacks and reduce the shared items to only include
        # whatever is in those sacks.
        for _ in range(3):
            shared_items = shared_items & set(rucksacks.pop())
        
        # Sum the priorities of all shared items and add it to the running total
        total_priority += sum(_get_priority(item) for item in shared_items)
    
    return total_priority

#---------------------------------------------------------------------------------------------------

def run(input_file):

    rucksacks = get_input(input_file)

    part_one(rucksacks)
    part_two(rucksacks)

from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict

#---------------------------------------------------------------------------------------------------

def _parse_stacks(lines):
    """ Parses the initial crate stacks configuration from the input, and returns a list of stacks
    of crates. """

    stacks_dict = defaultdict(list)
    
    # For each line in the problem input, until we reach a line containing the character '1'...
    lines_iter = iter(lines)
    while '1' not in (line := next(lines_iter)):
        
        # Consider 4 characters at a time from the line. Each chunk of 4 characters is potentially
        # a crate in the next stack. Start at stack #0.
        stack_ix = 0
        while line:
            
            # Peel off the remaining first 4 characters, which might represent a crate.
            # Remove bracket characters and leading/trailing whitespace.
            crate, line = line[:4], line[4:]
            crate = crate.replace('[', '').replace(']', '').strip()
            
            # If there's a character remaining, that's a crate, present in the stack at `stack_ix`
            if crate:
                stacks_dict[stack_ix].append(crate)
                
            # Increment which stack we might find a crate in during the next 4 characters we check.
            stack_ix += 1
    
    # We're parsing the input from the top of the stack to the bottom, but we want to treat the
    # stacks as stack data structures. To pull off the "top" of the stack we'll need to reverse
    # each stack of crates.
    for ix, crates in stacks_dict.items():
        stacks_dict[ix] = list(reversed(crates))
    
    # Create a list of stacks, and add an empty stack to the list for each key in the dictionary
    stacks = list()
    for _ in stacks_dict.keys():
        stacks.append(list())
    
    # Iterate over the keys (indices) in order and set that stack into the list.
    for stack_ix in sorted(stacks_dict.keys()):
        stacks[stack_ix] = stacks_dict[stack_ix]

    return stacks


def _parse_instruction(instruction_line):
    """ Parses the single instruction line. """

    # Remove the leading "move" and turn "from" and "to" into spaces
    instruction_line = instruction_line.replace('move ', '')
    instruction_line = instruction_line.replace(' from ', ' ')
    instruction_line = instruction_line.replace(' to ', ' ')

    # What remains just looks like "2 8 5", split on spaces and turn to ints
    number_of_crates, source, target = (int(n) for n in instruction_line.split())

    # We're zero-indexing the stacks so subtract 1 from the stack numbers
    return number_of_crates, source-1, target-1


def _parse_instructions(lines):
    """ Parses the input instructions and returns a list of tuples of number of crates to be moved,
    and the (zero-indexed) source stack and target stack numbers. """
    
    return [_parse_instruction(line) for line in lines if 'move' in line]


@aoc_output_formatter(2022, 5, 1, 'top crate on each stack', assert_answer='SHMSDGZVC')
def part_one(stacks, instructions):

    for n, source, target in instructions:

        # Move the top crate from the source stack to the target stack, `n` times
        for _ in range(n):
            e = stacks[source].pop()
            stacks[target].append(e)

    return ''.join(stack[-1] for stack in stacks)


@aoc_output_formatter(2022, 5, 2, 'CraneMover 9001 top crate on each stack', assert_answer='VRZGHDFBQ')
def part_two(stacks, instructions):

    for n, source, target in instructions:

        # Move the top `n` crates from the source stack to the target stack
        e = stacks[source][-1*n:]
        stacks[source] = stacks[source][:-1*n]
        stacks[target].extend(e)

    return ''.join(stack[-1] for stack in stacks)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    stacks = _parse_stacks(get_input(input_file))
    instructions = _parse_instructions(get_input(input_file))

    part_one(stacks, instructions)

    # Read the input again because we're modifying the line when parsing it in part 1.
    # Also reset the state of the stacks.
    stacks = _parse_stacks(get_input(input_file))
    instructions = _parse_instructions(get_input(input_file))

    part_two(stacks, instructions)

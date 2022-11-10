from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input
from util.iter import int_stream

#---------------------------------------------------------------------------------------------------

def _redistribute_memory(memory_banks):
    """ Continuously redistributes memory in the memory bank Mancala-style by finding the
    largest memory chunk, emptying it and stepwise adding a single block to the rest of the bank
    in order until the memory is gone.

    Continues until a memory bank configuration is seen that has already been seen before,
    indicating the memory redistribution has entered a cycle.

    Returns a tuple containing the number of steps until the cycle was entered, and the length of
    the cycle. """

    mem_size = len(memory_banks)

    # Store the memory states along with the step at which they were first seen.
    memory_states = dict()
    memory_states[tuple(memory_banks)] = 0

    # Start counting steps while shuffling memory around.
    for step in int_stream(1):

        # Find the largest chunk of memory in the bank, and its index.
        max_mem_value = max(memory_banks)
        max_mem_index = memory_banks.index(max_mem_value)

        # Clear out the memory at that index
        memory_banks[max_mem_index] = 0

        # Track how much memory we have left to distribute, and where we are in the memory bank
        curr_ix = max_mem_index
        remaining_blocks_to_distribute = max_mem_value

        while remaining_blocks_to_distribute > 0:
            # Proceed to the next memory location (looping around if necessary), add a block to
            # the current chunk of memory and decrement the remaining blocks to distribute
            curr_ix = (curr_ix + 1) % mem_size
            memory_banks[curr_ix] += 1
            remaining_blocks_to_distribute -= 1

        # Check if this state has already been seen before
        next_mem_state = tuple(memory_banks)
        if next_mem_state in memory_states:
            # If so, calculate the size of the cycle by substracting the step number of the first
            # time we saw this memory state from the current step.
            cycle_length = step - memory_states[next_mem_state]

            # Return the step number when we entered the cycle, and the length of the cycle
            return step, cycle_length
        else:
            # If not, add it to the dictionary along with this step when we first saw it
            memory_states[next_mem_state] = step


@aoc_output_formatter(2017, 6, 1, 'num memory redistribution steps before a cycle is entered')
def part_one(memory_banks):
    return _redistribute_memory(memory_banks)[0]


@aoc_output_formatter(2017, 6, 2, 'size of the memory redistribution cycle')
def part_two(memory_banks):
    return _redistribute_memory(memory_banks)[1]

#---------------------------------------------------------------------------------------------------

def run(input_file):

    memory_banks = get_tokenized_input(input_file, None, int)[0]

    part_one(memory_banks.copy())
    part_two(memory_banks.copy())

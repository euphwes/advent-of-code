from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from collections import defaultdict

#---------------------------------------------------------------------------------------------------

def __build_history(numbers):
    """ Take the starting numbers and build a number history; this is a map, where the key is each
    number spoken, and the value is a list of 1-indexed indices when that number was spoken. """

    history = defaultdict(list)
    for i, n in enumerate(numbers, 1):
        history[n].append(i)

    return history


def __play_memory_game_until_turn(starting_numbers, num_turns):
    """ Play the elvish memory game until the nth turn, and return the last number spoken. """

    turn    = len(starting_numbers) + 1
    spoken  = starting_numbers[-1]
    history = __build_history(starting_numbers)

    while turn <= num_turns:
        previous_num_history = history[spoken]

        if len(previous_num_history) == 1:
            spoken = 0
        else:
            spoken = previous_num_history[-1] - previous_num_history[-2]

        history[spoken].append(turn)
        turn += 1

    return spoken

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 15, 1, '2020th spoken number')
def part_one(numbers):
    return __play_memory_game_until_turn(numbers, 2020)


@aoc_output_formatter(2020, 15, 2, '30000000th spoken number')
def part_two(numbers):
    return __play_memory_game_until_turn(numbers, 30_000_000)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_tokenized_input(input_file, ',', int)[0])
    part_two(get_tokenized_input(input_file, ',', int)[0])

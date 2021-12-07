from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _fish_count_after_n_days_slow(fish, n):
    """ Slow/naive implementation which simulates the school of lanternfish and evaluates each fish
    one at a time, returning the number of fish after n days. """

    # Simulate for n days
    for _ in range(n):

        # Tracks the new lanterfish to be added after this day's simulation is done
        to_add = list()

        # Iterate every fish
        for i, x in enumerate(fish):
            if x == 0:
                # If their counter is 0, reset it to 6 and add a new fish with a counter of 8
                fish[i] = 6
                to_add.append(8)
            else:
                # otherwise reduce the counter by 1
                fish[i] -= 1

        # Add any new lanternfish born today to the school
        fish.extend(to_add)

    return len(fish)


def _fish_count_after_n_days_fast(fish, n):
    """ Fast implementation which simulates the school of lanternfish, returning the number of fish
    after n days. """

    # Take an initial count of how many fish have what internal counter values
    today_count = defaultdict(int)
    for f in fish:
        today_count[f] += 1

    # Simulate for n days
    for _ in range(n):

        # Tracks the number of fish with each internal counter value after the current day finishes
        tomorrow_count = defaultdict(int)

        # Each day, the fish with counters of 0 reset to 6 and create the same number of new fish
        # with counters at 8.
        tomorrow_count[8] = today_count[0]
        tomorrow_count[6] = today_count[0]

        # The rest of the fish (non-zero counters) have their counters decrease by 1.
        # Tomorrow, the number of fish with counter of n-1 is the same as number of fish today
        # with counter of n
        for n in range(1, 9):
            tomorrow_count[n-1] += today_count[n]

        # Update the number fish per counter value with tomorrow's count
        today_count = tomorrow_count

    # Sum and return the number of total fish
    return sum(n for _, n in today_count.items())


@aoc_output_formatter(2021, 6, '1 (naive)', 'lanterfish after 80 days')
def part_one_slow(fish):
    return _fish_count_after_n_days_slow(fish, 80)


@aoc_output_formatter(2021, 6, '1 (optimized)', 'lanterfish after 80 days')
def part_one_fast(fish):
    return _fish_count_after_n_days_fast(fish, 80)


@aoc_output_formatter(2021, 6, 2, 'lanterfish after 256 days')
def part_two(fish):
    return _fish_count_after_n_days_fast(fish, 256)


#---------------------------------------------------------------------------------------------------

def run(input_file):

    fish = [int(x) for x in get_input(input_file)[0].split(',')]

    # Copy the fish for part one (slow) because the list is modified while simulating
    part_one_slow([f for f in fish])
    part_one_fast(fish)
    part_two(fish)

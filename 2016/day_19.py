from math import floor, log

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 19
YEAR = 2016

PART_ONE_DESCRIPTION = "last elf standing, old rules"
PART_ONE_ANSWER = 1834903

PART_TWO_DESCRIPTION = "last elf standing, new rules"
PART_TWO_ANSWER = 1420280


def _A006257_josephus_closed_form(n):
    """Closed form of the Josephus problem, returns the "winner" given n participants.
    Solution sourced from https://oeis.org/A006257."""

    return 0 if n == 0 else 2 * (n - 2 ** int(log(n, 2))) + 1


def _simulate_bogus_white_elephant(number_elves):
    """Simulates the Josephus problem. For my problem input, this takes ~10s to run."""

    elves = list(range(number_elves))
    elf_count = number_elves

    ELF_OUT = "x"
    getter_ix = -1

    # While there are still elves playing...
    while elf_count > 1:
        # Find the "getter", the recipient of the presents, who is next elf who's still playing
        while True:
            getter_ix = (getter_ix + 1) % number_elves
            if elves[getter_ix] != ELF_OUT:
                break

        # Find the "sucker", the elf who's still playing that's about to lose all their presents
        sucker_ix = (getter_ix) % number_elves
        while True:
            sucker_ix = (sucker_ix + 1) % number_elves
            if elves[sucker_ix] != ELF_OUT:
                break

        # Mark the sucker as out, and decrement the elf count.
        elves[sucker_ix] = ELF_OUT
        elf_count -= 1

    # Find the only elf remaining and return his number (index + 1)
    return [e for e in elves if e != ELF_OUT][0] + 1


def _simulate_second_bogus_white_elephant(number_elves):
    """Simulates the Cowboy Shootout problem. For my problem input, this takes a very long time
    to complete, around 24 hours."""

    elves = list(range(number_elves))
    elf_count = number_elves

    # While there are still elves playing...
    while elf_count > 1:
        # The elf losing their presents is halfway across the circle, erring to the left for an
        # odd number of participants.
        sucker_ix = floor(elf_count / 2)

        # Remove the loser from the group.
        elves.pop(sucker_ix)
        elf_count -= 1

        # Shift all the elves so the next elf remaining is at the 0th index. This is why the
        # simulation is so slow... but the logic is cleaner and easier to read than maintaining
        # a moving pointer to the gift recipient elf index.
        first = elves[0]
        elves = elves[1:]
        elves.append(first)

    # Return the number (index + 1) of the only elf remaining
    return elves[0] + 1


def _A334473_cowboy_shootout_closed_form(n):
    """Closed form of the Cowboy Shootout problem, returns the "winner" given n participants.
    Solution sourced from https://oeis.org/A334473."""

    def highest_power_of_3(x):
        option = 0
        while 3**option <= x:
            option += 1
        return 3 ** (option - 1)

    x = highest_power_of_3(n)
    if x == n:
        return x
    else:
        if n < 2 * x:
            return n % x
        else:
            return x + 2 * (n % x)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(number_elves):
    # Initially simulated this problem, though the simulation is slow for a large number of
    # participants. I ran the simulation for a small number of participants (n between 1 and 20)
    # and got a hit at OEIS (Online Encyclopedia of Integer Sequences). Switched over to the
    # closed form of the solution which I sourced from there.

    # return _simulate_bogus_white_elephant(number_elves)
    return _A006257_josephus_closed_form(number_elves)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(number_elves):
    # Initially simulated this problem, though the simulation is slow for a large number of
    # participants. I ran the simulation for a small number of participants (n between 1 and 20)
    # and got a hit at OEIS (Online Encyclopedia of Integer Sequences). Switched over to the
    # closed form of the solution which I sourced from there.

    # return _simulate_second_bogus_white_elephant(number_elves)
    return _A334473_cowboy_shootout_closed_form(number_elves)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    number_elves = int(get_input(input_file)[0])

    part_one(number_elves)
    part_two(number_elves)

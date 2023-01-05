from collections import defaultdict

from util.decorators import aoc_output_formatter

DAY = 9
YEAR = 2018

PART_ONE_DESCRIPTION = "winning elf's score"
PART_ONE_ANSWER = 380705

PART_TWO_DESCRIPTION = "winning elf's score with 100x as many marbles"
PART_TWO_ANSWER = 3171801582


class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.last = self
        self.next = self


def _play_marble_game(num_elves, highest_marble):

    current_elf = -1
    curr_marble = LinkedListNode(0)

    elf_scores = defaultdict(int)

    for next_marble_value in range(1, highest_marble + 1):

        current_elf = (current_elf + 1) % num_elves

        if next_marble_value % 23 == 0:

            # Go back to the marble 7 behind the current
            for _ in range(7):
                curr_marble = curr_marble.last

            # Add the next marble and the 7-back marble's values to the current elf's score
            elf_scores[current_elf] += next_marble_value
            elf_scores[current_elf] += curr_marble.value

            # Remove the marble 7 back from the linked list
            old_next = curr_marble.next
            old_last = curr_marble.last

            old_last.next = old_next
            old_next.last = old_last

            # The new current marble is the one after the marble we just removed.
            curr_marble = old_next

        else:
            # Create a new linked list node for the next marble, and do standard doubly-linked
            # list stuff to insert it at the position 2 nodes ahead of the current node.
            new_marble = LinkedListNode(next_marble_value)

            new_last = curr_marble.next
            new_next = curr_marble.next.next

            new_last.next = new_marble
            new_next.last = new_marble

            new_marble.next = new_next
            new_marble.last = new_last

            # The new current marble is the one we just inserted.
            curr_marble = new_marble

    return elf_scores


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(num_elves, highest_marble):
    scores = _play_marble_game(num_elves, highest_marble)
    return max(scores.values())


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(num_elves, highest_marble):
    scores = _play_marble_game(num_elves, highest_marble)
    return max(scores.values())


# ----------------------------------------------------------------------------------------------


def run(_):

    num_elves = 464
    highest_marble = 71730

    part_one(num_elves, highest_marble)
    part_two(num_elves, highest_marble * 100)

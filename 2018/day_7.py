from collections import defaultdict
from string import ascii_uppercase
from typing import Optional

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 7
YEAR = 2018

PART_ONE_DESCRIPTION = "the order in which steps are completed"
PART_ONE_ANSWER = "GKCNPTVHIRYDUJMSXFBQLOAEWZ"

PART_TWO_DESCRIPTION = "how many seconds for 5 workers to complete time-bound work"
PART_TWO_ANSWER = 1265


def _parse_prereqs(raw_prereqs):
    """Parse the raw problem input to return a dictionary of step names mapped to a list of
    other prerequisite steps."""

    prerequisites = defaultdict(list)
    all_letters = set()

    for line in raw_prereqs:
        prereq = line[5]
        postreq = line[-12]
        prerequisites[postreq].append(prereq)

        all_letters.add(prereq)
        all_letters.add(postreq)

    # Some steps don't have prerequisites, so we represent their prereqs with an empty list.
    for letter in all_letters:
        if letter not in prerequisites.keys():
            prerequisites[letter] = list()

    return prerequisites


def _get_avail_next_step(prereqs, completed_steps, in_flight=None):
    """Given a set of prerequisites, completed steps and in-progress steps, return the next step
    which is available to complete (ties are broken alphabetically)."""

    if in_flight is None:
        in_flight = set()

    # Find all steps which haven't already been completed or are currently in-progress, and
    # which have all their prerequisites completed so they are available to be worked on.
    avail_next = list()
    for step, prereqs in prereqs.items():
        if step in completed_steps or step in in_flight:
            continue
        if all(p in completed_steps for p in prereqs):
            avail_next.append(step)

    # If no steps are currently available to be worked on, return None
    if not avail_next:
        return None

    # Otherwise sort the available steps alphabetically and return the first.
    avail_next.sort()
    return avail_next[0]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    ordered_steps = ""
    prerequisites = _parse_prereqs(stuff)

    while True:
        next_letter = _get_avail_next_step(prerequisites, set(ordered_steps))
        if not next_letter:
            return ordered_steps

        ordered_steps += next_letter


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    prerequisites = _parse_prereqs(stuff)

    class Worker:
        """A worker which can be idle, or working on a step with some duration remaining."""

        def __init__(self, letter, remaining):
            self.letter: Optional[str] = letter
            self.time_remaining = remaining

        @property
        def is_available(self):
            return self.letter is None

    workers = [Worker(None, 0) for _ in range(5)]

    completed_steps = set()

    # Keep ticking time away
    for i in int_stream():

        # For each worker...
        for worker in workers:

            # First see if it's working on something. If so, decrement the time by a second.
            # If that completes the step, add that step to the completed steps and mark this
            # worker as available by setting its step to None.
            if not worker.is_available:
                worker.time_remaining -= 1
                if worker.time_remaining == 0:
                    completed_steps.add(worker.letter)
                    worker.letter = None

            # If the worker is available, find the next available step which is not already
            # complete or in-progress, assign it to the worker with time remaining = 60 + the
            # letter's place in the alphabet.
            if worker.is_available:
                next_letter = _get_avail_next_step(
                    prerequisites,
                    completed_steps,
                    in_flight={w.letter for w in workers if w.letter},
                )
                if next_letter is None:
                    continue
                worker.letter = next_letter
                worker.time_remaining = 60 + 1 + ascii_uppercase.index(worker.letter)

        # Once we've completed all the steps, return how long it took.
        if len(completed_steps) == len(prerequisites.keys()):
            return i


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)
    part_one(stuff)
    part_two(stuff)

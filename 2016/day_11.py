from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappop, heappush
from itertools import combinations
from typing import Any

from util.decorators import aoc_output_formatter

DAY = 11
YEAR = 2016

PART_ONE_DESCRIPTION = "minimum steps"
PART_ONE_ANSWER = 31

PART_TWO_DESCRIPTION = "minimum steps for real layout"
PART_TWO_ANSWER = 55


states_seen = set()


@dataclass(order=True)
class PriorityStateGraphNode:
    priority: int
    elevator: int = field(compare=False)
    floors: Any = field(compare=False)
    depth: int


def _parse_floor(floor):
    """Determine which chips and generators are on the provided floor, returned as a tuple of
    (list_of_chip_elements, list_of_generator_elements)."""

    # Group the chips and generators, and strip the -g or -c tag so we have just the elements.
    chips = [item.replace("-c", "") for item in floor if item.endswith("-c")]
    generators = [item.replace("-g", "") for item in floor if item.endswith("-g")]

    return set(chips), set(generators)


def _score_state(e, floors):
    """Score this state of the board, where lower scores mean the board is closer to being
    scored. This score is used for the "priority" of the state when being placed into the heap
    to check."""

    # Elevator is weighted as 3 points per floor away from the top floor.
    score = (3 - e) * 3

    # Each chip or generator is weighted as 1 point per floor away from the top floor.
    for i, floor in enumerate(floors):
        score += len(floor) * (3 - i)

    return score


def _normalize_state(elevator, floors):
    """Takes in an elevator position and floor arrangement, and turns it into a representation
    which can be hashed so we can store previously-seen states in a set. Also considers the fact
    that there are multiple states which are equivalent to one another because any given pair
    of chips/generators are interchangeable with one another.

    Ex:
    floor1 contains (di-g, di-c, sr-g), floor2 contains (pl-g, pl-c, sr-c)
    is equivalent to
    floor1 contains (pl-g, pl-c, sr-g), floor2 contains (di-g, di-c, sr-g).

    Both states "hash" to ((1, 1), (1, 2), (2, 2)) because one pair is on floor 1, one pair on
    floor 2, and the remaining pair split between floor 1 and 2."""

    # For each element, build a tuple of (chip_floor, generator_floor)
    element_pair_locations = defaultdict(list)
    for i, floor in enumerate(floors):
        chips, generators = _parse_floor(floor)
        for element in chips:
            element_pair_locations[element].append(i)
        for element in generators:
            element_pair_locations[element].append(i)

    # For each tuple of (chip_floor, generator_floor), forget which pair it belongs to and stick
    # it in a list to sort by the location tuple values.
    pair_locations = list()
    for _, loc in element_pair_locations.items():
        pair_locations.append(tuple(loc))
    pair_locations.sort(key=lambda x: x[1])
    pair_locations.sort(key=lambda x: x[0])

    # Return a tuple of (elevator location, tuple of pair location tuples)
    return (elevator, tuple(pair_locations))


def _are_any_chips_gonna_fry(floor):
    """Checks the state of the floor and makes sure we won't have any microchips that are going to
    fry because they are left with another generator and not connected to their own generator."""

    chips, generators = _parse_floor(floor)

    # If there are no generators at all on this floor, that's fine. No chips will fry.
    if not generators:
        return False

    # If there are generators on this floor, every chip needs to have its own generator for shield.
    # For each chip, make sure it has its generator with it, otherwise that chip will fry.
    for element in chips:
        if element not in generators:
            return True

    # Every chip is with its generator, everything's ok.
    return False


def _get_available_floor_options(elevator, next_elevator, floors):
    """Returns possible floor states for the next step, given the current floor state, the current
    elevator position, and the next elevator position. The elevator takes 1-2 items with it and must
    ensure the departing floor and the arriving floor end up in a valid state."""

    next_floor_states = list()

    # The elevator needs to carry something with it to power it, so we have to choose at least one
    # thing, up to 2 things, from the current floor to carry with it.
    for n in (1, 2):
        for what_to_carry in combinations(floors[elevator], n):
            # Figure out what's left on the floor that the elevator is leaving. If anything's going
            # to fry because we're leaving it in a bad state, skip to the next option.
            floor_leaving = [
                item for item in floors[elevator] if item not in what_to_carry
            ]
            if _are_any_chips_gonna_fry(tuple(floor_leaving)):
                continue

            # Figure out what's going to be on the floor that the elevator is arriving at.
            # If anything's going to fry after we arrive, skip to the next option.
            floor_arriving = [item for item in floors[next_elevator]]
            floor_arriving.extend(what_to_carry)
            if _are_any_chips_gonna_fry(tuple(floor_arriving)):
                continue

            # If both the floor we're arriving at and the floor we're leaving are going to be ok,
            # then build up all the floors and append to the list of possible next floor states.
            new_floors = [floor for floor in floors]
            new_floors[elevator] = floor_leaving
            new_floors[next_elevator] = floor_arriving
            next_floor_states.append(new_floors)

    return next_floor_states


def _get_available_steps(elevator, floors):
    """Returns a list of tuples of the form (elevator, floors), which are possible next states for
    the facility to be in."""

    next_step_options = list()

    global states_seen

    # Figure out where the elevator can go next: up or down, but within the bounds of the first and
    # last floors. Note: there's an additional heuristic where you can omit the option to go down a
    # floor if all floors below are empty, but it doesn't make much difference in runtime for me.
    elevator_options = {
        0: [1],
        1: [0, 2],
        2: [1, 3],
        3: [2],
    }[elevator]

    for next_elevator in elevator_options:
        # Whichever floor the elevator might go to next, figure out what possible states the floors
        # can be at after the elevator makes that trip.
        floor_options = _get_available_floor_options(elevator, next_elevator, floors)
        for next_floor_state in floor_options:
            # If the this floor/elevator state option (or an equivalent state) has already been seen
            # before, then skip it.
            if _normalize_state(next_elevator, next_floor_state) in states_seen:
                continue
            next_step_options.append((next_elevator, next_floor_state))

    return next_step_options


def _is_solved(elevator, floors):
    """Returns if the elevator is at floor 4, along with all the generators and microchips."""

    return elevator == 3 and all(len(f) == 0 for f in floors[:-1])


def _calc_min_steps_to_solved(floors):
    """Calculate and return the minimum number of steps to move all the chips and generators safely
    to the fourth floor."""

    # Maintain a set of states already visited so we can prune these from the search space later.
    global states_seen
    states_seen = set()

    # We'll be breadth-first searching the state graph, and using a heap as a priority queue for
    # the states we haven't searched yet.
    state_queue = list()

    starting_state = PriorityStateGraphNode(_score_state(0, floors), 0, floors, 0)
    heappush(state_queue, starting_state)

    while state_queue:
        state = heappop(state_queue)

        if _is_solved(state.elevator, state.floors):
            return state.depth

        for e, f in _get_available_steps(state.elevator, state.floors):
            states_seen.add(_normalize_state(e, f))
            new_state = PriorityStateGraphNode(
                _score_state(e, f), e, f, state.depth + 1
            )
            heappush(state_queue, new_state)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(floors):
    return _calc_min_steps_to_solved(floors)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(floors):
    return _calc_min_steps_to_solved(floors)


def run(input_file):

    # Not going to parse that nonsense, let's just set it up manually.
    # Thulium = tm
    # Plutonium = pu
    # Strontium = sr
    # Promethium = pm
    # Ruthenium = ru
    part1_floors = [
        ["tm-g", "tm-c", "pu-g", "sr-g"],  # 1st floor
        ["pu-c", "sr-c"],  # 2nd floor
        ["pm-g", "pm-c", "ru-g", "ru-c"],  # 3rd floor
        [],  # 4th floor
    ]
    part_one(part1_floors)

    # Thulium = tm
    # Plutonium = pu
    # Strontium = sr
    # Promethium = pm
    # Ruthenium = ru
    # Elerium = em
    # Dilithium = di
    part2_floors = [
        ["tm-g", "tm-c", "pu-g", "sr-g", "em-g", "em-c", "di-g", "di-c"],
        ["pu-c", "sr-c"],
        ["pm-g", "pm-c", "ru-g", "ru-c"],
        [],
    ]
    part_two(part2_floors)

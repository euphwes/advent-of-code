from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream
from .common_2017 import _rotate

from dataclasses import dataclass
from string import ascii_lowercase

#---------------------------------------------------------------------------------------------------

@dataclass
class Spin:
    steps: int

    def enact(self, dancers):
        return _rotate(dancers, self.steps)


@dataclass
class Exchange:
    """ Swaps dancers at the two specified indices. """

    index_a: int
    index_b: int

    def enact(self, dancers):
        dancer_at_a = dancers[self.index_a]
        dancer_at_b = dancers[self.index_b]

        dancers[self.index_a] = dancer_at_b
        dancers[self.index_b] = dancer_at_a

        return dancers


@dataclass
class Partner:
    """ Swaps dancers with the two specified names. """

    partner_a: int
    partner_b: int

    def enact(self, dancers):
        index_of_a = dancers.index(self.partner_a)
        index_of_b = dancers.index(self.partner_b)

        dancers[index_of_a] = self.partner_b
        dancers[index_of_b] = self.partner_a

        return dancers


def _parse_choreography(raw_choreography):
    """ Parse the problem input into Swap, Exchange, and Partner dance steps. """

    choreography_steps = list()

    for dance_step in raw_choreography:
        command, rest = dance_step[0], dance_step[1:]

        if command == 's':
            choreography_steps.append(Spin(int(rest)))

        elif command == 'x':
            index_a, index_b = [int(ix) for ix in rest.split('/')]
            choreography_steps.append(Exchange(index_a, index_b))

        elif command == 'p':
            partner_a, partner_b = rest.split('/')
            choreography_steps.append(Partner(partner_a, partner_b))

    return choreography_steps


@aoc_output_formatter(2017, 16, 1, 'final dancer arrangement')
def part_one(raw_choreography):

    dancers = list(ascii_lowercase[:16])
    choreography = _parse_choreography(raw_choreography)

    for dance_step in choreography:
        dancers = dance_step.enact(dancers)

    return ''.join(dancers)


@aoc_output_formatter(2017, 16, 2, 'final dancer arrangement after 1 billion dances')
def part_two(raw_choreography):

    dancers = list(ascii_lowercase[:16])
    choreography = _parse_choreography(raw_choreography)

    # The set to hold quick lookup if we've seen this state of dancers before, after a full dance
    # has finished. The list (history) is to hold an ordered record of the states of the dancers
    # after each dance.
    dancer_state_set = {tuple(dancers)}
    dancer_state_history = list([''.join(dancers)])

    class FoundCycleException(BaseException):
        pass

    # Keep running dance after dance until we find a state we've seen before.
    try:
        for _ in int_stream():
            for dance_step in choreography:
                dancers = dance_step.enact(dancers)

            # After the dance finishes, see if we've seen this state of dancers before.
            dancer_state = tuple(dancers)
            if dancer_state in dancer_state_set:
                # If so, break out of the infinite loop
                raise FoundCycleException()
            else:
                # If not, store the dancer state in the set and append this state to the ordered
                # history of states we've seen.
                dancer_state_set.add(dancer_state)
                dancer_state_history.append(''.join(dancer_state))
    except FoundCycleException:
        pass

    # The 1 billionth state of the daners will be the modulus of 1 billion % cycle length, because
    # every cycle_length times we'll circle back and start the cycle of dancer states all over
    return dancer_state_history[1_000_000_000 % len(dancer_state_history)]

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw_choreography = get_input(input_file)[0].split(',')

    part_one(raw_choreography)
    part_two(raw_choreography)

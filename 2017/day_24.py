from util.decorators import aoc_output_formatter
from util.input import get_input

from dataclasses import dataclass

#---------------------------------------------------------------------------------------------------

# Global variable where we can store all the bridges we enumerate, so we only have to do it once.
# Don't want to calculate it once per part since it's expensive.
all_bridges = None

@dataclass
class Connector:
    port_1: int
    port_2: int

    @staticmethod
    def from_definition(line):
        port_1, port_2 = (int(n) for n in line.split('/'))
        return Connector(port_1=port_1, port_2=port_2)

    @property
    def ports(self):
        return [self.port_1, self.port_2]

    @property
    def strength(self):
        return sum(self.ports)

    def connects_to_port(self, other_port):
        return other_port in self.ports


def get_bridges_for_open_port(open_port, remaining_connectors):
    """ For a given open port and a set of connectors which haven't been used yet, return a list of
    all possible bridges (chained connectors off this open port). """

    # Figure out which connectors of the ones remaining connect to this open port.
    candidates = [x for x in remaining_connectors if x.connects_to_port(open_port)]

    # Base recursive case, nothing left connects to the open port, return an empty list.
    if not candidates:
        return list()

    # Hold all the bridges we can build off this open port.
    bridges = list()

    # For every connector in the candidates...
    for next_connector in candidates:

        # The candidate next connector itself is a possible bridge (of length 1).
        bridges.append([next_connector])

        # For this next connector, figure out what the new open port will be.
        # Ex: For an open port of 3, and a connector 3/5, the 3 of the connector will connect to
        # the open port, and the new open port is 5.
        ports = next_connector.ports
        ports.remove(open_port)
        next_open_port = ports[0]

        # Recursively figure out what chains we can build off the new open port.
        
        # The new remaining connectors don't include the connector we just picked.
        reduced_connectors = [c for c in remaining_connectors if c is not next_connector]

        # For each sub_bridge which can be built from the new open port, we add it (with the new
        # connector in front of it) as a possible bridge for this new connector.
        for sub_bridge in get_bridges_for_open_port(next_open_port, reduced_connectors):
            bridges.append([next_connector] + sub_bridge)

    return bridges


def _get_bridge_strength(bridge):
    """ Utility function to get the total bridge strength. """

    return sum(connector.strength for connector in bridge)


@aoc_output_formatter(2017, 24, 1, 'max bridge strength', assert_answer=1695)
def part_one(connectors):

    global all_bridges
    all_bridges = get_bridges_for_open_port(0, connectors)

    return max(_get_bridge_strength(bridge) for bridge in all_bridges)


@aoc_output_formatter(2017, 24, 2, 'strength of longest bridge', assert_answer=1673)
def part_two(connectors):

    global all_bridges

    # Sort all bridges by their length
    all_bridges.sort(key=len)

    # Find the length of the longest bridges, and consider only the longest bridges
    max_length = len(all_bridges[-1])
    longest_bridges = [bridge for bridge in all_bridges if len(bridge) == max_length]

    return max(_get_bridge_strength(bridge) for bridge in longest_bridges)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    connectors = [Connector.from_definition(line) for line in get_input(input_file)]

    part_one(connectors)
    part_two(connectors)

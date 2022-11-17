from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

from dataclasses import dataclass
from collections import defaultdict

#---------------------------------------------------------------------------------------------------

@dataclass
class FirewallLayerInfo:
    scan_range: int
    layer_depth: int

    @property
    def cycle_length(self):
        # Because the scanner oscillates back and forth across its range, it actually takes
        # (scan_range * 2) - 2 time steps to reach its starting position, so let's call that the
        # cycle length because that's what matters when determining if a packet gets caught.
        return (self.scan_range * 2) - 2

    def is_caught(self, picoseconds):
        # A packet is caught if it arrives here at a timestep where the scanner has completed its
        # cycle and is back to the starting postition.
        return picoseconds % self.cycle_length == 0

    def get_severity(self, picoseconds):
        # If a packet is caught, the "severity" is this firewall scanner's depth * scan range
        return 0 if not self.is_caught(picoseconds) else self.layer_depth * self.scan_range


class PassthroughFirewallLayer:
    """ A firewall layer representation for layers where no scanner is present. """
    def is_caught(self, picoseconds):
        return False
    def get_severity(self, picoseconds):
        return 0


def _parse_firewall_info(raw_firewall_info):
    """ Parse the problem input and build a map of firewall layer depth to FirewallLayerInfo. """

    # Default to a passthrough on firewall layers with no scanner.
    firewall_info = defaultdict(PassthroughFirewallLayer)

    for layer in raw_firewall_info:
        depth, range = (int(piece) for piece in layer.split(': '))
        firewall_info[depth] = FirewallLayerInfo(scan_range=range, layer_depth=depth)

    return firewall_info


@aoc_output_formatter(2017, 13, 1, 'severity accumulated during trip that leaves immediately')
def part_one(raw_firewall_info):
    depth_to_info_map = _parse_firewall_info(raw_firewall_info)
    final_depth = max(depth_to_info_map.keys())

    packet_location = -1
    accumulated_severity = 0

    while packet_location < final_depth:
        packet_location += 1
        accumulated_severity += depth_to_info_map[packet_location].get_severity(packet_location)

    return accumulated_severity


@aoc_output_formatter(2017, 13, 2, 'num picoseconds delay where the packet is not caught')
def part_two(raw_firewall_info):
    depth_to_info_map = _parse_firewall_info(raw_firewall_info)
    final_depth = max(depth_to_info_map.keys())

    for delay in int_stream():
        packet_location = -1
        was_caught = False

        while packet_location < final_depth:
            packet_location += 1
            if depth_to_info_map[packet_location].is_caught(packet_location+delay):
                was_caught = True
                break

        if not was_caught:
            return delay

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw_firewall_info = get_input(input_file)

    part_one(raw_firewall_info)
    part_two(raw_firewall_info)

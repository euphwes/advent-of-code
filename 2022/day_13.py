from util.decorators import aoc_output_formatter
from util.input import get_input, safe_eval

DAY = 13
YEAR = 2022

PART_ONE_DESCRIPTION = "sum of indices of packets in the correct order"
PART_ONE_ANSWER = 6046

PART_TWO_DESCRIPTION = "decoder key for the distress signal"
PART_TWO_ANSWER = 21423


def _compare(left_list, right_list):
    """Compare two lists using the rules defined in https://adventofcode.com/2022/day/13,
    and return whether the left list is "less than" the right list."""

    for i in range(len(left_list)):
        # For each element in list a, extract the element at the same index in list b.
        left_lement = left_list[i]
        try:
            right_element = right_list[i]
        except IndexError:
            # If the left list runs out of items first, then the two lists are not in order.
            return False

        # If both elements are integers, we can compare them directly. If the elements are
        # equal, move to the next, otherwise return whether the left list's value is less than
        # the right's.
        if isinstance(left_lement, int) and isinstance(right_element, int):
            if left_lement == right_element:
                continue
            return left_lement < right_element

        # If we have a mix of integers and lists at this index, convert the integers to lists of
        # length 1 containing just that integer.
        if isinstance(left_lement, int):
            left_lement = [left_lement]
        if isinstance(right_element, int):
            right_element = [right_element]

        # Now we have only lists, and we can recursively compare the two. If the recursive check
        # is not able to determine if the two inner lists are in order, the elements are equal
        # (like two identical ints), so we continue to the next item in the outer list.
        retval = _compare(left_lement, right_element)
        if retval is not None:
            return retval
        continue

    # If we've reached this point, all elements compared so far are identical and no ordering
    # determination can be made.

    # If there are fewer elements in the left list a than in right list b, the left list ran out
    # first and thus the lists a and b are in order.
    if len(left_list) < len(right_list):
        return True

    # If the lengths are the same, we can't make an ordering determination, return None.
    return None


class Packet:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return _compare(self.value, other.value)


def _parse_packets(raw_packets):
    """Parses Packets out of the raw problem input."""

    packets = list()

    for line in raw_packets:
        if not line:
            continue
        packets.append(Packet(safe_eval(line)))

    return packets


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_packets):

    indices = list()
    packets = _parse_packets(raw_packets)

    ix = 1
    while packets:
        # Grab the next pair of packets from the front of the list and compare them.
        packet_a = packets.pop(0)
        packet_b = packets.pop(0)

        # If they're in order, add the current pair of packets' index to the list
        if packet_a < packet_b:
            indices.append(ix)

        ix += 1

    return sum(indices)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_packets):

    # Special packets used to calculate distress signal.
    divider_a = [[2]]
    divider_b = [[6]]

    # Parse the packets and then add the two divider signal packets to the overall list.
    packets = _parse_packets(raw_packets)
    packets.append(Packet(divider_a))
    packets.append(Packet(divider_b))

    # Sort the packets (using the _compare function implemented for relative ordering)
    # and then extract the (ordered) raw packet values back out.
    packets.sort()
    packet_values = [p.value for p in packets]

    # Find the 1-based indices of the two divider packets, and return their product.
    divider_a_ix = packet_values.index(divider_a) + 1
    divider_b_ix = packet_values.index(divider_b) + 1

    return divider_a_ix * divider_b_ix


# ----------------------------------------------------------------------------------------------


def run(input_file):

    raw_packets = get_input(input_file)

    part_one(raw_packets)
    part_two(raw_packets)

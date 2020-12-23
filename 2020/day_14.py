from util.decorators import aoc_output_formatter
from util.input import get_input

from itertools import product

#---------------------------------------------------------------------------------------------------

def __to_binary(n):
    """ Returns the decimal integer n represented in binary as a string, zero-padded to 36 bits. """

    return bin(n)[2:].zfill(36)


def __to_decimal(value):
    """ Accepts a binary representation of an integer, and converts back to decimal. """

    return int(value, 2)


def __apply_mask(value, mask):
    """ Accepts a binary representation of an integer, and a bitmask to apply to it. Applies the
    bitmask and then returns the new binary string. """

    new_value = list()
    for i, mask_character in enumerate(mask):
        if mask_character == 'X':
            new_value.append(value[i])
        else:
            new_value.append(mask_character)

    return ''.join(new_value)


def __apply_address_mask(value, mask):
    """ Accepts a binary representation of an integer, and a bitmask to apply to it. Applies the
    bitmask and then returns the new binary string, with floating values reprented by X. """

    new_value = list()
    for i, mask_character in enumerate(mask):
        if mask_character == '0':
            new_value.append(value[i])
        else:
            new_value.append(mask_character)

    return ''.join(new_value)


def __get_memory_address_and_value(line):
    """ Accepts an input line and parses out the memory address and value to be inserted there. """

    parts = line.split('] = ')
    address = int(parts[0].replace('mem[', ''))
    value = int(parts[1])

    return address, value

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 14, 1, 'sum of values in memory')
def part_one(input_lines):
    memory = dict()
    for line in input_lines:
        if line.startswith('mask = '):
            mask = line.replace('mask = ', '')
            continue

        address, value = __get_memory_address_and_value(line)

        masked_value = __apply_mask(__to_binary(value), mask)
        masked_decimal = __to_decimal(masked_value)

        memory[address] = masked_decimal

    return sum(memory.values())


@aoc_output_formatter(2020, 14, 2, 'sum of values in memory')
def part_two(input_lines):
    memory = dict()
    for line in input_lines:
        if line.startswith('mask = '):
            mask = line.replace('mask = ', '')
            continue

        address, value = __get_memory_address_and_value(line)

        # Apply the mask to the memory address, which will return a bit string with some X bits
        # which indicate "floating bits" that take on all possible values.
        masked_address = __apply_address_mask(__to_binary(address), mask)

        # Count the number of floating bits
        num_floating_bits = sum(1 for char in masked_address if char == 'X')

        # Iterate over all possible combinations of values for the number of floating bits.
        for bits in map(list, product(range(2), repeat=num_floating_bits)):

            # Make a copy of the memory address, and list-ify it so we can modify it
            # Once we apply the bits to the masked address, this is one possible value that the
            # floating masked address can take.
            new_address = list(masked_address)

            # While there's still a floating bit in the mem address, take the first bit left from
            # the combination of bit values and replace the floating bit with it.
            # Ex: address = 'X0X1X', bits = '110', take 1 off the front, replace the first X with it
            # ->  address = '10X1X', bits = '10', take 1 off the front, replace the first X with it
            # ->  address = '1011X', bits = '0', take 0 off the front, replace the first X with it
            # ->  address = '10110', bits = '', address is complete
            while 'X' in new_address:
                bit = bits.pop(0)
                new_address[new_address.index('X')] = str(bit)

            # Turn the bitstring into a decimal memory address, and write the value to that address
            address_value = __to_decimal(''.join(new_address))
            memory[address_value] = value

    return sum(memory.values())

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

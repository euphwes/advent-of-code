from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict
from string import ascii_lowercase

#---------------------------------------------------------------------------------------------------

class DecodedRoom:
    def __init__(self, encrypted_room):
        self.checksum = encrypted_room[-6:-1]
        self.sector_id = int(encrypted_room[-10:-7])
        self.room_name = encrypted_room[:-11]
        self.decoded_room_name = self._decode_room_name()


    def is_real_room(self):
        """ Returns if this room's provided checksum matches its calculated checksum. """

        # Count the number of occurences of each letter, ignoring hyphens
        letter_frequency = defaultdict(int)
        for char in [c for c in self.room_name if c != '-']:
            letter_frequency[char] += 1

        # Turn the letter/count dict into a list of tuples of the form (count, letter)
        frequency_to_letter_list = [(count, letter) for letter, count in letter_frequency.items()]

        # Sort alphabetically first, then by count large-to-small
        frequency_to_letter_list.sort(key = lambda count_letter: count_letter[1])
        frequency_to_letter_list.sort(key = lambda count_letter: count_letter[0], reverse=True)

        # The first 5 elements will be the most common letters, ties sorted alphabetically
        # Those first 5 characters are the checksum, compare them to the real checksum
        calculated_checksum = ''.join([k for _, k in frequency_to_letter_list][:5])
        return calculated_checksum == self.checksum


    def _decode_room_name(self):
        decoded_room_name = list()
        for char in self.room_name:
            if char == '-':
                decoded_room_name.append(' ')
            else:
                start_ix = ascii_lowercase.index(char)
                rotated_ix = (start_ix + self.sector_id) % 26
                decoded_room_name.append(ascii_lowercase[rotated_ix])
        return ''.join(decoded_room_name)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2016, 4, 1, 'sum of sector IDs of real rooms')
def part_one(encrypted_rooms):
    decoded_rooms = [DecodedRoom(room) for room in encrypted_rooms]
    return sum([room.sector_id for room in decoded_rooms if room.is_real_room()])


@aoc_output_formatter(2016, 4, 2, 'sector ID of room where the North Pole objects are stored')
def part_two(encrypted_rooms):
    for room in [DecodedRoom(room) for room in encrypted_rooms]:
        # After checking for rooms with 'north' in the name, the only room that matches is
        # 'northpole object storage'.
        if 'north' in room.decoded_room_name:
            return room.sector_id

#---------------------------------------------------------------------------------------------------

def run(input_file):

    encrypted_rooms = get_input(input_file)

    part_one(encrypted_rooms)
    part_two(encrypted_rooms)

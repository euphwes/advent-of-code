from hashlib import md5

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 5
YEAR = 2016

PART_ONE_DESCRIPTION = "door password"
PART_ONE_ANSWER = "f97c354d"

PART_TWO_DESCRIPTION = "second door password"
PART_TWO_ANSWER = "863dde27"

_md5 = lambda x: md5(x.encode()).hexdigest()


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(door_id):

    print("\nHacking door #1 password...")
    door_password = ""
    for index in int_stream(0):
        if (hash := _md5(door_id + str(index))).startswith("00000"):
            door_password += hash[5]
            print(door_password)

        if len(door_password) == 8:
            print("")  # to make the "hacking" look nicer in the terminal
            return door_password


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(door_id):

    print("\nHacking door #2 password...")
    door_password = list("________")
    for index in int_stream(0):
        if (hash := _md5(door_id + str(index))).startswith("00000"):
            try:
                position = int(hash[5])
                char_value = hash[6]
                if position <= 7 and door_password[position] == "_":
                    door_password[position] = char_value
                    print("".join(door_password))
            except ValueError:
                continue

            if not "_" in door_password:
                print("")  # to make the "hacking" look nicer in the terminal
                return "".join(door_password)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    door_id = get_input(input_file)[0]

    part_one(door_id)
    part_two(door_id)

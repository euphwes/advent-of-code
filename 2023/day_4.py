from util.decorators import aoc_output_formatter
from util.input import get_input
from collections import defaultdict

DAY = 4
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = 18619

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = 8063216


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    p = 0

    for line in stuff:
        h1, h2 = line.split(" | ")
        h1 = h1.split(": ")[1]

        winning_nums = list()
        my_cards = list()

        for n in h1.split():
            winning_nums.append(int(n))

        for n in h2.split():
            my_cards.append(int(n))

        match_count = 0
        for n in my_cards:
            if n in winning_nums:
                match_count += 1

        if match_count > 0:
            p += 2 ** (match_count - 1)

    return p


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    card_counts = defaultdict(lambda: 1)

    for line in stuff:
        h1, h2 = line.split(" | ")
        card_num, h1 = h1.split(": ")
        card_num = int(card_num.replace("Card ", ""))

        if card_num not in card_counts.keys():
            card_counts[card_num] = 1

        winning_nums = list()
        my_cards = list()

        for n in h1.split():
            winning_nums.append(int(n))

        for n in h2.split():
            my_cards.append(int(n))

        match_count = 0
        for n in my_cards:
            if n in winning_nums:
                match_count += 1

        if match_count > 0:
            for _ in range(card_counts[card_num]):
                for i in range(match_count):
                    card_counts[card_num + i + 1] = card_counts[card_num + i + 1] + 1

    return sum(card_counts.values())


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)

    part_one(stuff)
    part_two(stuff)

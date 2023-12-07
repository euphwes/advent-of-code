from util.decorators import aoc_output_formatter
from util.input import get_input
from collections import defaultdict

DAY = 4
YEAR = 2023

PART_ONE_DESCRIPTION = "point total of all scratchcards"
PART_ONE_ANSWER = 18619

PART_TWO_DESCRIPTION = "total number of scratchcards we have"
PART_TWO_ANSWER = 8063216


def _parse_scratchcard(raw_scratchcard):
    """Parses a raw scratchcard line from the input. Returns a tuple containing the card number,
    a set of the winning numbers, and a list of our numbers on that card.

    Ex: Card 6: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    --> (
            6,
            {41, 48, 83, 86, 17},
            [83, 86, 6, 31, 17, 9, 48, 53]
        )
    """

    first_half, raw_my_picks = raw_scratchcard.split(" | ")
    card_num, raw_winning_nums = first_half.split(": ")
    card_num = int(card_num.replace("Card ", ""))

    winning_nums = {int(n) for n in raw_winning_nums.split()}
    my_nums = [int(n) for n in raw_my_picks.split()]

    return (
        card_num,
        winning_nums,
        my_nums,
    )


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(lottery_cards):
    points_total = 0

    # For each scratch card...
    for raw_card in lottery_cards:
        _, winning_nums, my_nums = _parse_scratchcard(raw_card)

        # ...count the number of my winning number matches in that card.
        number_matching_numbers = 0
        for n in my_nums:
            if n in winning_nums:
                number_matching_numbers += 1

        # The first match is worth a point, each additional match doubles the number of points.
        if number_matching_numbers > 0:
            points_total += 2 ** (number_matching_numbers - 1)

    return points_total


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(lottery_cards):
    # Remember how many of each card we have.
    card_counts = defaultdict(lambda: 1)

    # For each lottery card...
    for raw_card in lottery_cards:
        card_num, winning_nums, my_nums = _parse_scratchcard(raw_card)

        # ...count the number of my winning number matches in that card.
        match_count = 0
        for n in my_nums:
            if n in winning_nums:
                match_count += 1

        # For each copy of this card, add that many copies to the next N scratch cards,
        # where N is the number of matches on this card.
        for i in range(match_count):
            card_counts[card_num + i + 1] += card_counts[card_num]

    return sum(card_counts.values())


# ----------------------------------------------------------------------------------------------


def run(input_file):
    lottery_cards = get_input(input_file)

    part_one(lottery_cards)
    part_two(lottery_cards)

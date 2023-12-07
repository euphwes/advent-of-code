from dataclasses import dataclass, field
from collections import Counter
from enum import Enum
from typing import Dict, Tuple, List

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 7
YEAR = 2023

PART_ONE_DESCRIPTION = "total winnings of card hands"
PART_ONE_ANSWER = 250898830

PART_TWO_DESCRIPTION = "total winnings of card hands, jokers wild"
PART_TWO_ANSWER = 252127335


CARD_VALUES: Dict[str, int] = {card: i for i, card in enumerate("23456789TJQKA")}
CARD_VALUES_WILD: Dict[str, int] = {card: i for i, card in enumerate("J23456789TQKA")}


class CamelCardsGameType(Enum):
    NORMAL = "normal"
    JOKERS_WILD = "jokers_wild"


class CamelCardsHandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


HAND_TYPE_BY_CARD_COUNTS: Dict[Tuple[int, ...], CamelCardsHandType] = {
    (5,): CamelCardsHandType.FIVE_OF_A_KIND,
    (4, 1): CamelCardsHandType.FOUR_OF_A_KIND,
    (3, 2): CamelCardsHandType.FULL_HOUSE,
    (3, 1, 1): CamelCardsHandType.THREE_OF_A_KIND,
    (2, 2, 1): CamelCardsHandType.TWO_PAIR,
    (2, 1, 1, 1): CamelCardsHandType.ONE_PAIR,
    (1, 1, 1, 1, 1): CamelCardsHandType.HIGH_CARD,
}


@dataclass
class CamelCardsHand:
    bet: int
    cards: str
    game_type: CamelCardsGameType

    # The type of hand, and the tie breaker, change depending on the game type.
    # We'll calculate those after we create the hand.
    hand_type: CamelCardsHandType = field(init=False)
    tie_breaker: List[int] = field(init=False)

    def __post_init__(self):
        # The tie breaker is just the value of each card, in the order they appear in your hand,
        # but the values for the a "J" (jack/joker) depend on whether jokers are wild.
        values = (
            CARD_VALUES
            if self.game_type == CamelCardsGameType.NORMAL
            else CARD_VALUES_WILD
        )
        self.tie_breaker = [values[card] for card in self.cards]

        # Determine the hand type. If jokers are not wild, count the number of all types of
        # cards and use that to determine the hand type. Aka (4, 1) means 4 of some type of
        # card, and 1 of another, which is four of a kind.
        #
        # If jokers are wild, figure out the best possible hand type possible if those jokers
        # can take on the type as another card.
        counts = tuple(sorted(Counter(self.cards).values(), reverse=True))
        self.hand_type = (
            HAND_TYPE_BY_CARD_COUNTS[counts]
            if self.game_type == CamelCardsGameType.NORMAL
            else self.get_best_hand_type_with_jokers_wild()
        )

    def get_best_hand_type_with_jokers_wild(self) -> CamelCardsHandType:
        """Returns the best possible CamelCardsHandType if you consider the jokers in this hand
        to be some other type of card instead."""

        # Extract the non-joker cards.
        non_jokers = [c for c in self.cards if c != "J"]

        # If there are either 0 jokers or 5 jokers, we don't need to try the various hands
        # possibilities that the jokers give us. If there are no jokers, nothing is wild, and
        # the hand is just what we have. If all 5 cards are jokers, then the best hand is always
        # a five of a kind.
        if len(non_jokers) in (0, 5):
            counts = tuple(sorted(Counter(self.cards).values(), reverse=True))
            return HAND_TYPE_BY_CARD_COUNTS[counts]

        possible_hands = list()

        # Figure out all possible hand types we can get if we consider the jokers to be some
        # other type of card.
        #
        # There's no point in selecting different types of cards for each joker, the best hand
        # is always going to have as many of a single type of card as possible.
        #
        # Furthermore we should only consider considering jokers to be a type of card we already
        # have in our hand, because that'll give us the highest possible number of any single
        # card.
        for joker_alt in non_jokers:
            possible_hands.append(
                CamelCardsHand(
                    bet=self.bet,
                    cards=self.cards.replace("J", joker_alt),
                    game_type=CamelCardsGameType.NORMAL,
                )
            )

        # Sort the hands and return the best hand's type.
        possible_hands.sort()
        return possible_hands[-1].hand_type

    def __lt__(self, other: "CamelCardsHand"):
        """Define a comparison operator between CamelCardsHand instances, so we can sort them
        relative to each other."""

        # If the hand types of the two hands are not equivalent, compare them directly.
        if self.hand_type != other.hand_type:
            return self.hand_type.value < other.hand_type.value

        # If the hand types are equivalent, compare the tie breakers isntead.
        return self.tie_breaker < other.tie_breaker


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(camel_cards_hands):
    # Parse each line of the input into a list of Camel Cards hands.
    hands = list()
    for line in camel_cards_hands:
        cards, bet = line.split()
        hands.append(
            CamelCardsHand(
                bet=int(bet),
                cards=cards,
                game_type=CamelCardsGameType.NORMAL,
            )
        )

    # Sort the hands relative to each other, and count winnings.
    # Each hand wins its bet * its overall position in the set of hands (1-indexed).
    winnings = 0
    for i, h in enumerate(sorted(hands)):
        winnings += (i + 1) * h.bet

    return winnings


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(camel_cards_hands):
    # Parse each line of the input into a list of Camel Cards hands, jokers wild.
    hands = list()
    for line in camel_cards_hands:
        cards, bet = line.split()
        hands.append(
            CamelCardsHand(
                bet=int(bet),
                cards=cards,
                game_type=CamelCardsGameType.JOKERS_WILD,
            )
        )

    # Sort the hands relative to each other, and count winnings.
    # Each hand wins its bet * its overall position in the set of hands (1-indexed).
    winnings = 0
    for i, h in enumerate(sorted(hands)):
        winnings += (i + 1) * h.bet

    return winnings


# ----------------------------------------------------------------------------------------------


def run(input_file):
    camel_cards_hands = get_input(input_file)

    part_one(camel_cards_hands)
    part_two(camel_cards_hands)

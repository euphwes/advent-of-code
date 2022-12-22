from enum import Enum

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 2
YEAR = 2022

PART_ONE_DESCRIPTION = "total score"
PART_ONE_ANSWER = 10994

PART_TWO_DESCRIPTION = "total score with correct interpretation"
PART_TWO_ANSWER = 12526


class MatchOutcome(Enum):
    WIN = "win"
    TIE = "tie"
    LOSE = "lose"


class RockPaperScissorsHand(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


LETTER_HAND_MAP = {
    "A": RockPaperScissorsHand.ROCK,
    "X": RockPaperScissorsHand.ROCK,
    "B": RockPaperScissorsHand.PAPER,
    "Y": RockPaperScissorsHand.PAPER,
    "C": RockPaperScissorsHand.SCISSORS,
    "Z": RockPaperScissorsHand.SCISSORS,
}


HAND_SCORE_MAP = {
    RockPaperScissorsHand.ROCK: 1,
    RockPaperScissorsHand.PAPER: 2,
    RockPaperScissorsHand.SCISSORS: 3,
}


OUTCOME_SCORE_MAP = {
    MatchOutcome.WIN: 6,
    MatchOutcome.TIE: 3,
    MatchOutcome.LOSE: 0,
}


# Utility map which denotes winning rock paper scissors matchups, with the outcome from
# the perspective of the hand that's the key in the dictionary.
KEY_HAND_WINS_MAP = {
    RockPaperScissorsHand.ROCK: RockPaperScissorsHand.SCISSORS,
    RockPaperScissorsHand.PAPER: RockPaperScissorsHand.ROCK,
    RockPaperScissorsHand.SCISSORS: RockPaperScissorsHand.PAPER,
}

# Flip the above map to get a map of losing matchups from the perspective of the key hand.
KEY_HAND_LOSES_MAP = {
    value_hand: key_hand for key_hand, value_hand in KEY_HAND_WINS_MAP.items()
}


def evaluate_match(my_hand, other_hand):
    """Evaluate a rock paper scissors match and return the outcome from the perspective of the
    first argument."""

    if my_hand == other_hand:
        return MatchOutcome.TIE

    if KEY_HAND_WINS_MAP[my_hand] == other_hand:
        return MatchOutcome.WIN

    return MatchOutcome.LOSE


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(strategy_guide):
    score = 0

    for match in strategy_guide:
        other_hand, my_hand = [LETTER_HAND_MAP[hand] for hand in match.split()]
        match_outcome = evaluate_match(my_hand, other_hand)

        score += HAND_SCORE_MAP[my_hand]
        score += OUTCOME_SCORE_MAP[match_outcome]

    return score


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(strategy_guide):
    score = 0

    # Utility map to determine the target outcome of the match (from my POV) based on the letter
    # in the strategy guide.
    required_outcome = {
        "X": MatchOutcome.LOSE,
        "Y": MatchOutcome.TIE,
        "Z": MatchOutcome.WIN,
    }

    for match in strategy_guide:
        # From the match info, determine the other player's hand and what the desired outcome
        # of the match is (from my perspective).
        other_hand = LETTER_HAND_MAP[match.split()[0]]
        desired_outcome = required_outcome[match.split()[1]]

        # If I'm supposed to tie, we have the same hand.
        if desired_outcome == MatchOutcome.TIE:
            my_hand = other_hand

        # If I'm supposed to win, the other player will lose, so look up my hand based on theirs
        elif desired_outcome == MatchOutcome.WIN:
            my_hand = KEY_HAND_LOSES_MAP[other_hand]

        # If I'm supposed to lose, the other player will win, so look up my hand based on theirs
        else:
            my_hand = KEY_HAND_WINS_MAP[other_hand]

        score += HAND_SCORE_MAP[my_hand]
        score += OUTCOME_SCORE_MAP[desired_outcome]

    return score


# ----------------------------------------------------------------------------------------------


def run(input_file):

    strategy_guide = get_input(input_file)

    part_one(strategy_guide)
    part_two(strategy_guide)

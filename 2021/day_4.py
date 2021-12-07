from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

#---------------------------------------------------------------------------------------------------

_MARKED = 'X'


def _apply_number(num, board):
    """ Apply a number to the bingo board by seeing if the number is on the board, and if so,
    marking it. """

    for y, row in enumerate(board):
        for x, board_number in enumerate(row):
            if board_number == num:
                # If the number matches, mark it and return early.
                # Bingo boards only have a number at most once.
                board[y][x] = _MARKED
                return


def _check_if_winner(board):
    """ Check if the bingo board is a winner. """

    # First check each row to see if any are entirely marked
    for row in board:
        if all(number == _MARKED for number in row):
            return True

    # Then check each column to see if any are entirely marked
    for i in range(5):
        column = [row[i] for row in board]
        if all(number == _MARKED for number in column):
            return True

    # Nope, not a winner
    return False


def _sum_unmarked(board):
    """ Returns the sum of all the unmarked spaces on a bingo board. """

    unmarked_sum = 0
    for row in board:
        unmarked_sum += sum([value for value in row if value != _MARKED])
    return unmarked_sum


@aoc_output_formatter(2021, 4, 1, 'final score of the first winning board')
def part_one(numbers, boards):
    for n, b in nested_iterable(numbers, boards):
        _apply_number(n, b)
        if _check_if_winner(b):
            return _sum_unmarked(b) * n


@aoc_output_formatter(2021, 4, 2, 'final score of the last winning board')
def part_two(numbers, boards):

    # Track the winning boards' scores, inserted in the order in which they win.
    # Track which boards have already won, so we don't add them to the winners twice.
    winners = list()
    winners_ix = set()

    for n in numbers:
        for i, b in enumerate(boards):
            _apply_number(n, b)
            # If the board hasn't already won, and is a winner, append its score to the list
            if (i not in winners_ix) and _check_if_winner(b):
                winners_ix.add(i)
                winners.append(_sum_unmarked(b) * n)

    # Take the score of the most recent (the last) board to win
    return winners[-1]

#---------------------------------------------------------------------------------------------------

def run(input_file):

    lines = get_input(input_file)

    bingo_numbers = [int(x) for x in lines[0].split(',')]

    boards = list()
    boards_workspace = [line for line in lines[1:] if line]

    while True:
        new_board = list()
        for line in boards_workspace[0:5]:
            row = [int(y) for y in line.split(' ') if y]
            new_board.append(row)
        boards.append(new_board)

        boards_workspace = boards_workspace[5:]
        if not boards_workspace:
            break

    part_one(bingo_numbers, boards)
    part_two(bingo_numbers, boards)

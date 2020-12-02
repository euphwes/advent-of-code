from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def __does_password_satisfy_incorrect_policy(line):
    """ Parses an incorrect password policy and corresponding password out a line from the input.
    Returns true if the password satisfies the incorrect policy. """

    # ex: 9-14 w: qwwwwwlwbwwwwswww
    policy, password = line.split(': ')

    # Extract the target letter, and the range of expected occurences of that letter in the password
    target_range, target_letter = policy.split(' ')
    lower, upper = (int(val) for val in target_range.split('-'))

    # Count the number of occurrences of the target letter in the password.
    # The password satisfies this policy if the number of occurences falls in the specified range.
    num_occurrences = sum(1 for letter in password if letter == target_letter)
    return num_occurrences in list(range(lower, upper+1))


def __does_password_satisfy_policy(line):
    """ Parses a password policy and corresponding password out a line from the input. Returns a
    tuple of the password and a function which checks if that password is valid according to the
    policy. """

    # ex: 9-14 w: qwwwwwlwbwwwwswww
    policy, password = line.split(': ')

    # Extract the target letter, and the password indices to check for that letter.
    target_indices, target_letter = policy.split(' ')
    target_indices = (int(val) for val in target_indices.split('-'))

    def __check_letter(i):
        """ Checks a specific index of the password. Returns true if the character at that 1-index
        position matches the target letter. Returns false if it does not, or if the index is outside
        the range of the password. """
        if i > len(password):
            return False
        return password[i-1] == target_letter

    # The password satisfies the policy if the target letter is at exactly 1 of the target indices
    return sum(1 for i in target_indices if __check_letter(i)) == 1

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 2, 1, 'number of valid passwords')
def part_one(puzzle_input):
    password_results = [__does_password_satisfy_incorrect_policy(line) for line in puzzle_input]
    return sum(1 for result in password_results if result)


@aoc_output_formatter(2020, 2, 2, 'number of actually valid passwords')
def part_two(puzzle_input):
    password_results = [__does_password_satisfy_policy(line) for line in puzzle_input]
    return sum(1 for result in password_results if result)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

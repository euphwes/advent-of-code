# Start by copying your 2023 day 2 input into a file called "day_2_input.txt", in the same
# folder as this file (day_2_part_1.py).
#
# Run this file by executing:
# python day_2_part_1.py
#
# (from the terminal, in the same folder as this file)

with open("day_2_input.txt", "r") as input_file:
    # Read all the lines of the input file, getting a list of strings
    raw_file_lines = input_file.readlines()

    # Remove the trailing newline characters at the end of each line.
    # Now we have a list of strings from our input, each element is a line from the file.
    #
    # Ex:
    # cube_game_info = [
    #     "Game 1: 1 blue; 5 blue; 11 red, 11 green",
    #     "Game 2: 17 red, 10 green; 3 blue, 17 red, 7 green",
    #     "Game 3: 10 blue, 3 green, 8 red; 15 green, 14 blue, 1 red",
    # ]
    cube_game_info = [line.replace("\n", "") for line in raw_file_lines]


# Hold the list of "powers" of the games. Per the part two description, the "power" of a game
# is the product of the minimum number of blocks of each color to make that game possible.
# If a game requires 3 blue blocks, 4 red blocks, and 10 green blocks, the power of that
# game is 3*4*10 = 120
powers = list()

# For each game in the list...
for game_line in cube_game_info:
    minimum_counts_by_block_color = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }

    # Split the line into halves; the first contains the game ID, the second contains
    # the info about the number of colored blocks pulled during each round.
    #
    # Ex:
    # "Game 9: 1 green, 5 blue; 4 blue; 2 red, 1 blue"
    #
    # After the split(": "), we ignore the game ID (don't need it in part 2), and the second
    # part is the
    # raw_block_pulls = "1 green, 5 blue; 4 blue; 2 red, 1 blue"
    _, raw_block_pulls = game_line.split(": ")

    # Split the half of the line containing the block pull info into a list of rounds
    # Ex:
    # "1 green, 5 blue; 4 blue; 2 red, 1 blue"
    #
    # After the split("; ") we have a list of 3 strings, each of which describes how many
    # blocks of each color were pulled in that round.
    #
    # block_pulls = [
    #     "1 green, 5 blue",   # 1 green, 5 blue blocks pulled in the first round
    #     "4 blue",            # 4 blue blocks pulled in the second round
    #     "2 red, 1 blue"      # 2 red, 1 blue block pulled in the third round
    # ]
    block_pulls = raw_block_pulls.split("; ")

    # For each round of block pulls...
    for pull in block_pulls:
        # Split that round into chunks that indicate the count of each colored block pulled.
        # Ex:
        # "1 green, 5 blue"
        #
        # After the split(", ") we have a list of 2 strings with count and color of blocks.
        # block_counts = ["1 green", "5 blue"]
        block_counts = pull.split(", ")

        # For each count of a block color pulled during this round...
        for d in block_counts:
            # Split on the space to get the color, and the number of blocks of that color
            # Ex:
            # "5 blue"
            #
            # After the split(" ") we have
            # num = 5
            # color = "blue"
            num, color = d.split(" ")
            num = int(num)

            # If the number of blocks of this color is higher than the minimum we know we
            # need for this color so far, this number is now the new minimum.
            if num > minimum_counts_by_block_color[color]:
                minimum_counts_by_block_color[color] = num

    game_power = 1
    for block_count in minimum_counts_by_block_color.values():
        game_power = game_power * block_count
    powers.append(game_power)

# The sum of all the game powers is the answer to part 2
sum_of_powers = sum(powers)
print(f"\n2023 Day 2 Part 2 answer: {sum_of_powers}")

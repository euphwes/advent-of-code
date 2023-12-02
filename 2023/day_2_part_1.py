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


# Hold a map that specifies how many of each color block we have available to us.
counts_by_block_color = {
    "red": 12,
    "green": 13,
    "blue": 14,
}
possible_game_ids = list()

# Assume each game is possible until we prove otherwise.
for game_line in cube_game_info:
    is_possible = True

    # Split the line into halves; the first contains the game ID, the second contains
    # the info about the number of colored blocks pulled during each round.
    #
    # Ex:
    # "Game 9: 1 green, 5 blue; 4 blue; 2 red, 1 blue"
    #
    # After the split(": ")
    # game_id = "Game 9"
    # raw_block_pulls = "1 green, 5 blue; 4 blue; 2 red, 1 blue"
    raw_game_id, raw_block_pulls = game_line.split(": ")

    # Strip off the word "Game" at the front and turn the remainder into an integer game ID
    game_id = int(raw_game_id.replace("Game ", ""))

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

            # If the number of blocks of this color is higher than the number of blocks
            # we know we actually have of this color, we know this game is impossible.
            if num > counts_by_block_color[color]:
                is_possible = False

    # For this particular game, if we know it's possible, add its game ID to the list of
    # possible game IDs.
    if is_possible:
        possible_game_ids.append(game_id)

# The sum of the game IDs which are possible is the answer to part 1
game_ids_sum = sum(possible_game_ids)
print(f"\n2023 Day 2 Part 1 answer: {game_ids_sum}")

from util.decorators import aoc_output_formatter
from util.input import get_input


DAY = 21
YEAR = 2018

PART_ONE_DESCRIPTION = "value for register 0 to halt in the fewest instructions"
PART_ONE_ANSWER = 9107763

PART_TWO_DESCRIPTION = "value for register 0 to halt in the most instructions"
PART_TWO_ANSWER = 7877093

# Full input below, we're going to reverse engineer the faux assembly
# enough to write an equivalent program in Python and then figure out
# how to make it halt.

# ip 2
# seti 123 0 3
# bani 3 456 3
# eqri 3 72 3
# addr 3 2 2
# seti 0 0 2
# seti 0 6 3
# bori 3 65536 4
# seti 7041048 8 3
# bani 4 255 5
# addr 3 5 3
# bani 3 16777215 3
# muli 3 65899 3
# bani 3 16777215 3
# gtir 256 4 5
# addr 5 2 2
# addi 2 1 2
# seti 27 6 2
# seti 0 1 5
# addi 5 1 1
# muli 1 256 1
# gtrr 1 4 1
# addr 1 2 2
# addi 2 1 2
# seti 25 1 2
# addi 5 1 5
# seti 17 8 2
# setr 5 2 4
# seti 7 9 2
# eqrr 3 0 5
# addr 5 2 2
# seti 5 3 2

# ----------

# Start decoding behavior, give jump targets "labels" for control flow reference.
# IP register is 2

# Variables are R0, R1, R3, R4, R5

# 00 seti 123 0 3      --           R3 = 123
# 01 bani 3 456 3      -- [LABEL_A] R3 = (R3 & 456)
# 02 eqri 3 72 3       --           R3 = 1 if R3 == 72 else 0
# 03 addr 3 2 2        --           R2 = R2 + R3
#                            ... basically IP += 1 if R3 == 1 which it will on first pass
#                            ... otherwise IP doesn't change.
#                            ... If R3 == 1, GOTO [LABEL_B]
# 04 seti 0 0 2        --           R2 = 0 GOTO [LABEL_A]
# 05 seti 0 6 3        -- [LABEL_B] R3 = 0
# 06 bori 3 65536 4    -- [LABEL_M] R4 = R3 | 65536
# 07 seti 7041048 8 3  --           R3 = 7041048
# 08 bani 4 255 5      -- [LABEL_K] R5 = R4 & 255
# 09 addr 3 5 3        --           R3 = R3 + R5
# 10 bani 3 16777215 3 --           R3 = R3 & 16777215
# 11 muli 3 65899 3    --           R3 = R3 * 65899
# 12 bani 3 16777215 3 --           R3 = R3 & 16777215
# 13 gtir 256 4 5      --           R5 = 1 if 256 > R4 else 0
# 14 addr 5 2 2        --           IP += R5
#                                      if R5 == 0 --> go to next
#                                      if R5 == 1 --> GOTO [LABEL_C]
# 15 addi 2 1 2        --           IP += 1
#                                      aka GOTO [LABEL_D]
# 16 seti 27 6 2       -- [LABEL_C] IP = 27
#                                      aka GOTO [LABEL_E]
# 17 seti 0 1 5        -- [LABEL_D] R5 = 0
# 18 addi 5 1 1        -- [LABEL_J] R1 = R5 + 1
# 19 muli 1 256 1      --           R1 = R1 * 256
# 20 gtrr 1 4 1        --           R1 = 1 if R1 > R4 else 0
# 21 addr 1 2 2        --           IP += R1
#                                      aka if R1 == 1, GOTO [LABEL_F]
#                                      but if R1 == 0, go to next
# 22 addi 2 1 2        --           IP += 1
#                                      aka GOTO [LABEL_G]
# 23 seti 25 1 2       -- [LABEL_F] IP = 25
#                                      aka GOTO [LABEL_H]
# 24 addi 5 1 5        -- [LABEL_G] R5 += 1
# 25 seti 17 8 2       --           IP = 17
#                                      aka GOTO [LABEL_J]
# 26 setr 5 2 4        -- [LABEL_H] R4 = R5
# 27 seti 7 9 2        --           IP = 7
#                                      aka GOTO [LABEL_K]
# 28 eqrr 3 0 5        -- [LABEL_E] R5 = 1 if R3 == R0 else 0
# 29 addr 5 2 2        --           IP += R5
#                                      aka END PROGRAM if R5 == 1
#                                      else if R5 == 0, keep going
# 30 seti 5 3 2        --           IP = 5
#                                      aka GOTO [LABEL_M]

# ----------

# Simplify
# IP register is 2

# Variables are R0, R1, R3, R4, R5

# 00 seti 123 0 3      --           R3 = 123
# 01 bani 3 456 3      -- [LABEL_A] R3 = (R3 & 456)
# 02 eqri 3 72 3       --           R3 = 1 if R3 == 72 else 0
#
#                                   -- start of IF statement
# 03 addr 3 2 2        --           IP += R3
# 04 seti 0 0 2        --           R2 = 0 GOTO [LABEL_A]
#                                   -- end of IF statement
#
#                                   if R3 == 0:
#                                      go back to [LABEL_A] (like a while loop)
#                                   else:
#                                      break out of the loop and go to the next statement
#                                      aka [LABEL_B]
#
# 05 seti 0 6 3        -- [LABEL_B] R3 = 0
# 06 bori 3 65536 4    -- [LABEL_M] R4 = R3 | 65536
# 07 seti 7041048 8 3  --           R3 = 7041048
# 08 bani 4 255 5      -- [LABEL_K] R5 = R4 & 255
# 09 addr 3 5 3        --           R3 = R3 + R5
# 10 bani 3 16777215 3 --           R3 = R3 & 16777215
# 11 muli 3 65899 3    --           R3 = R3 * 65899
# 12 bani 3 16777215 3 --           R3 = R3 & 16777215
# 13 gtir 256 4 5      --           R5 = 1 if 256 > R4 else 0
#
#                                   -- start of IF statement
# 14 addr 5 2 2        --           IP += R5
#                                      if R5 == 0 --> go to next
#                                      if R5 == 1 --> GOTO [LABEL_C]
# 15 addi 2 1 2        --           IP += 1
#                                      aka GOTO [LABEL_D]
# 16 seti 27 6 2       -- [LABEL_C] IP = 27
#                                      aka GOTO [LABEL_E]
#                                   -- end of complicated multi-jump IF statement
#
#                                   if R5 == 0:
#                                      # GOTO [LABEL_D]
#                                      # logic from D inserted here and removed later
#                                      #
#                                      R5 = 0
#                                      [LABEL_J] R1 = R5 + 1
#                                      R1 = R1 * 256
#                                      R1 = 1 if R1 > R4 else 0
#                                      if R1 == 0:
#                                          # GOTO [LABEL_G] logic inserted here
#                                          R5 += 1
#                                          GOTO [LABEL_J], few lines above
#                                      else:
#                                          R4 = R5
#                                          GOTO [LABEL_K] many lines above
#                                   else:
#                                      # GOTO [LABEL_E]
#                                      # logic from E inserted here and removed later
#                                      #
#                                      if R3 == R0:
#                                          END PROGRAM
#                                      else:
#                                          GOTO [LABEL_M]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one():

    def _rewritten_assembly_program():
        # First while-loop omitted because the bitwise AND is properly implemented,
        # and so the loop exits immediately and sets R3 back to zero. The effect is
        # that all registers just start at 0 when the "real" program starts.

        # We're looking for the *first* value of R0 that causes the program to halt.
        R0 = 0

        # All other registers start at 0.
        R1 = 0
        R3 = 0
        R4 = 0
        R5 = 0

        while True:
            R4 = R3 | 65536
            R3 = 7041048

            while True:
                R5 = R4 & 255
                R3 = R3 + R5
                R3 = ((R3 & 16777215) * 65899) & 16777215

                if 256 > R4:
                    # When we reach this point, the assembly program exits if R3 == R0.
                    # Just return the current value of R3 right now, which is the first
                    # value of R0 that would cause the assembly program to exit.
                    return R3

                    # if R3 == R0:
                    #     # ** END PROGRAM **
                    #     return
                    # else:
                    #     break

                else:
                    R5 = 0
                    while True:
                        R1 = R5 + 1
                        R1 = R1 * 256

                        if R1 > R4:
                            R4 = R5
                            break

                        else:
                            R5 += 1
                            continue

    return _rewritten_assembly_program()


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two():

    def _rewritten_assembly_program():
        # First while-loop omitted because the bitwise AND is properly implemented,
        # and so the loop exits immediately and sets R3 back to zero. The effect is
        # that all registers just start at 0 when the "real" program starts.

        # We're looking for the *last* value of R0 that causes the program to halt.
        R0 = 0

        # All other registers start at 0.
        R1 = 0
        R3 = 0
        R4 = 0
        R5 = 0

        # Helpers so we can identify when we start repeating R3 values.
        r3_values_seen = list()
        r3_values_set = set()

        while True:
            R4 = R3 | 65536
            R3 = 7041048

            while True:
                R5 = R4 & 255
                R3 = R3 + R5
                R3 = ((R3 & 16777215) * 65899) & 16777215

                if 256 > R4:
                    # When we reach this point, the assembly program exits if R3 == R0.
                    # Let's record all values of R3 we see, until we see one we've already
                    # seen before (meaning the program would be entering a cycle). Once we
                    # hit that point, return the *previous* value of R3, which is the most
                    # recent new one, and is therefore the R3/R0 value that causes the
                    # program to halt after the highest number of executed instructions.
                    if R3 in r3_values_set:
                        return r3_values_seen[-1]
                    else:
                        r3_values_seen.append(R3)
                        r3_values_set.add(R3)

                    if R3 == R0:
                        # ** END PROGRAM **
                        return
                    else:
                        break

                else:
                    R5 = 0
                    while True:
                        R1 = R5 + 1
                        R1 = R1 * 256

                        if R1 > R4:
                            R4 = R5
                            break

                        else:
                            R5 += 1
                            continue

    return _rewritten_assembly_program()


# ----------------------------------------------------------------------------------------------


def run(_):
    part_one()
    part_two()

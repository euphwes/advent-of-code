from math import ceil, sqrt

from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembly import AssemblyComputer

DAY = 19
YEAR = 2018

PART_ONE_DESCRIPTION = "Value in register 0 if it starts with 0"
PART_ONE_ANSWER = 888

PART_TWO_DESCRIPTION = "Value in register 0 if it starts with 1"
PART_TWO_ANSWER = 10708992


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_program):
    computer = AssemblyComputer(raw_program)
    computer.run()
    return computer.registers[0]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_program):
    # computer = AssemblyComputer(raw_program)
    # computer.registers[0] = 1
    # computer.run()
    # return computer.registers[0]

    # Unaltered instructions
    # ip 4
    # addi 4 16 4
    # seti 1 4 3
    # seti 1 3 5
    # mulr 3 5 1
    # eqrr 1 2 1
    # addr 1 4 4
    # addi 4 1 4
    # addr 3 0 0
    # addi 5 1 5
    # gtrr 5 2 1
    # addr 4 1 4
    # seti 2 9 4
    # addi 3 1 3
    # gtrr 3 2 1
    # addr 1 4 4
    # seti 1 6 4
    # mulr 4 4 4
    # addi 2 2 2
    # mulr 2 2 2
    # mulr 4 2 2
    # muli 2 11 2
    # addi 1 2 1
    # mulr 1 4 1
    # addi 1 7 1
    # addr 2 1 2
    # addr 4 0 4
    # seti 0 8 4
    # setr 4 3 1
    # mulr 1 4 1
    # addr 4 1 1
    # mulr 4 1 1
    # muli 1 14 1
    # mulr 1 4 1
    # addr 2 1 2
    # seti 0 3 0
    # seti 0 6 4

    # ----------

    # Start decoding behavior, give jump targets "labels" for control flow reference.
    # IP register is 4

    # Variables are R0, R1, R2, R3, R5

    # 00 addi 4 16 4  --- [LABEL_A] Add 16 to the IP, skip to [LABEL_B]
    # 01 seti 1 4 3   --- [LABEL_D] Set register 3 = 1
    # 02 seti 1 3 5   --- [LABEL_J] Set register 5 = 1
    # 03 mulr 3 5 1   --- [LABEL_H] register 1 = register 3 * register 5
    # 04 eqrr 1 2 1   --- if register 1 == register 2
    #                     , set register 1 = 1, otherwise register 1 = 0
    # 05 addr 1 4 4   --- add value of register 1 to IP (either 0 or 1) -- basically, skip next
    #                     instruction if register 1 == 1
    # 06 addi 4 1 4       register 4 += 1 aka skip to [LABEL_F]
    # 07 addr 3 0 0       [LABEL_E] register 0 = register 0 + register 3
    # 08 addi 5 1 5       [LABEL_F] register 5 += 1
    # 09 gtrr 5 2 1       set register 1 = 1 if register 5 > register 2, otherwise set r1 = 0
    # 10 addr 4 1 4       add value of register 1 to IP (either 0 or 1) -- basically skip
    #                     next instruction if register 1 == 1. If R1 == 1, goto LABEL_G
    # 11 seti 2 9 4       set IP to 2 aka goto [LABEL_H]
    # 12 addi 3 1 3       [LABEL_G] register 3 += 1
    # 13 gtrr 3 2 1       register 1 = 1 if register 3 > register 3, else register 1 = 0
    # 14 addr 1 4 4       -- add register 0 to IP (either 0 or 1).
    # 15 seti 1 6 4       -- if r1 == 0: IP = 1, aka goto [LABEL_J]
    # 16 mulr 4 4 4       -- else: complete program (IP is set to 16*16 = 256)
    # 17 addi 2 2 2   --- [LABEL_B] Add 2 to register 2
    # 18 mulr 2 2 2   --- Multiply register 2 by register 2
    # 19 mulr 4 2 2   --- Multiply register 4 (IP) by 2, store in register 2, aka set register 2 = 76
    # 20 muli 2 11 2  --- register 2 = 11 * register 2, aka set register 2 = 836
    # 21 addi 1 2 1   --- register 1 = register 1 + 2
    # 22 mulr 1 4 1   --- register 1 = register 1 * IP aka register 1 * 22
    # 23 addi 1 7 1   --- register 1 = register 1 + 7
    # 24 addr 2 1 2   --- register 2 = register 1 + register 2
    # 25 addr 4 0 4   --- skip ahead X instructions where X is register 0's value
    #                  , aka skip to [LABEL_C] if register 0 == 1
    # 26 seti 0 8 4   --- set IP to the value in register 0
    # 27 setr 4 3 1   --- [LABEL_C] take IP and set it to register 1 aka register 1 = 27 (explicit set)
    # 28 mulr 1 4 1   --- register 1 = register 1 * register 4 aka register 1 *= 28
    # 29 addr 4 1 1   --- register 1 = register 4 + register 1 aka register 1 += 29
    # 30 mulr 4 1 1   --- register 1 = register 4 * register 1 aka register 1 *= 30
    # 31 muli 1 14 1  --- register 1 *= 14
    # 32 mulr 1 4 1   --- register 1 = register 1 * register 4 aka register 1 *= 32
    # 33 addr 2 1 2   --- register 2 = register 2 + register 1
    # 34 seti 0 3 0   --- set register 0 = 0
    # 35 seti 0 6 4   --- set register 4 = 0 IP = 0, go to [LABEL_D]

    # ----------

    # Simplify
    # IP register is 4

    # Variables are R0, R1, R2, R3, R5

    # 00 addi 4 16 4  --- [LABEL_A] Add 16 to the IP, skip to [LABEL_B]
    # 01 seti 1 4 3   --- [LABEL_D] R3 = 1
    # 02 seti 1 3 5   --- [LABEL_J] R5 = 1
    # 03 mulr 3 5 1   --- [LABEL_H] R1 = R3 * R5
    # 04 eqrr 1 2 1   --- R1 = 1 if R1 == R2 else 0
    #
    #                     -- start of IF statement
    # 05 addr 1 4 4   --- IP += R1
    # 06 addi 4 1 4       register 4 += 1 aka skip to [LABEL_F]
    # 07 addr 3 0 0       [LABEL_E] register 0 = register 0 + register 3
    # 08 addi 5 1 5       [LABEL_F] register 5 += 1
    #                     -- end of IF statement
    #
    #                     if R1 == 0:
    #                         R5 += 1
    #                     else:
    #                         R0 += R3
    #                         R5 += 1
    #
    # 09 gtrr 5 2 1       R1 = 1 if R5 > R2 else 0
    #
    #                     -- start of IF statement
    # 10 addr 4 1 4       IP += R1 add value of register 1 to IP (either 0 or 1) -- basically skip
    #                     next instruction if register 1 == 1. If R1 == 1, goto LABEL_G
    # 11 seti 2 9 4       GOTO [LABEL_H] (continue inside loop?)
    # 12 addi 3 1 3       [LABEL_G] register 3 += 1
    #                     -- end of IF statement
    #
    #                     if R1 == 0:
    #                         GOTO [LABEL_H]  (break? continue?)
    #                     else:
    #                         R3 += 1
    #
    #                     -- start of IF statement
    # 13 gtrr 3 2 1       R1 = 1 if R3 > R2 else 0
    # 14 addr 1 4 4       IP += R1 -- add register 0 to IP (either 0 or 1).
    # 15 seti 1 6 4       -- if r1 == 0: IP = 1, aka goto [LABEL_J]
    # 16 mulr 4 4 4       -- else: complete program (IP is set to 16*16 = 256)
    #                     -- start of IF statement
    #
    #                     if R1 == 0:
    #                         GOTO [LABEL_J]
    #                     else:
    #                         PROGRAM COMPLETE
    #
    # 17 addi 2 2 2   --- [LABEL_B] R2 += 2
    # 18 mulr 2 2 2   --- R2 *= R2
    # 19 mulr 4 2 2   --- R2 *= 19
    # 20 muli 2 11 2  --- R2 *= 11
    #
    # 21 addi 1 2 1   --- R1 = R1 + 2
    # 22 mulr 1 4 1   --- R1 *= 22
    # 23 addi 1 7 1   --- R1 += 7
    # 24 addr 2 1 2   --- R2 = R1 + R2
    #
    #                     -- start of IF statement
    # 25 addr 4 0 4   --- skip ahead X instructions where X is register 0's value
    #                  , aka skip to [LABEL_C] if register 0 == 1
    # 26 seti 0 8 4   --- set IP to the value in register 0
    # 27 setr 4 3 1   --- [LABEL_C] take IP and set it to register 1 aka register 1 = 27 (explicit set)
    #                     -- end of IF statement
    #
    #                     if R0 == 0:
    #                         # set IP = 0
    #                         GOTO [LABEL_D]
    #
    #                     R1 = 27
    #
    # 28 mulr 1 4 1   --- R1 *= 28
    # 29 addr 4 1 1   --- R1 += 29
    # 30 mulr 4 1 1   --- R1 *= 30
    # 31 muli 1 14 1  --- R1 *= 14
    # 32 mulr 1 4 1   --- R1 *= 32
    #
    # 33 addr 2 1 2   --- R2 += R1
    # 34 seti 0 3 0   --- R0 = 0
    # 35 seti 0 6 4   --- GOTO [LABEL_D]

    # ----------

    # Let's turn this into Python

    # Starting state of registers
    # R0 = 1
    # R1 = 0
    # R2 = 0
    # R3 = 0
    # R5 = 0

    # LABEL B, initial data setup
    # R2 += 2
    # R2 *= R2
    # R2 *= 19
    # R2 *= 11

    # R1 += 2
    # R1 *= 22
    # R1 += 7

    # R2 += R1

    # Now here we skip to the top if R0 == 0, but for part 2, R0 == 1, so we keep going...
    # R1 = 27
    # R1 *= 28
    # R1 += 29
    # R1 *= 30
    # R1 *= 14
    # R1 *= 32

    # R2 += R1

    # So basically LABEL B puts the registers into this state before going to LABEL D
    # R0 = 1
    # R1 = 10550400
    # R2 = 10551287
    # R3 = 0
    # R5 = 0

    # Re-paste for reference
    # 01 seti 1 4 3   --- [LABEL_D] R3 = 1
    # 02 seti 1 3 5   --- [LABEL_J] R5 = 1
    # 03 mulr 3 5 1   --- [LABEL_H] R1 = R3 * R5
    # 04 eqrr 1 2 1   --- R1 = 1 if R1 == R2 else 0
    #
    #                     -- start of IF statement
    # 05 addr 1 4 4   --- IP += R1
    # 06 addi 4 1 4       register 4 += 1 aka skip to [LABEL_F]
    # 07 addr 3 0 0       [LABEL_E] register 0 = register 0 + register 3
    # 08 addi 5 1 5       [LABEL_F] register 5 += 1
    #                     -- end of IF statement
    #
    #                     if R1 == 0:
    #                         R5 += 1
    #                     else:
    #                         R0 += R3
    #                         R5 += 1
    #
    # 09 gtrr 5 2 1       R1 = 1 if R5 > R2 else 0
    #
    #                     -- start of IF statement
    # 10 addr 4 1 4       IP += R1 add value of register 1 to IP (either 0 or 1) -- basically skip
    #                     next instruction if register 1 == 1. If R1 == 1, goto LABEL_G
    # 11 seti 2 9 4       GOTO [LABEL_H] (continue inside loop?)
    # 12 addi 3 1 3       [LABEL_G] register 3 += 1
    #                     -- end of IF statement
    #
    #                     if R1 == 0:
    #                         GOTO [LABEL_H]  (break? continue?)
    #                     else:
    #                         R3 += 1
    #
    #                     -- start of IF statement
    # 13 gtrr 3 2 1       R1 = 1 if R3 > R2 else 0
    # 14 addr 1 4 4       IP += R1 -- add register 0 to IP (either 0 or 1).
    # 15 seti 1 6 4       -- if r1 == 0: IP = 1, aka goto [LABEL_J]
    # 16 mulr 4 4 4       -- else: complete program (IP is set to 16*16 = 256)
    #                     -- start of IF statement
    #
    #                     if R1 == 0:
    #                         GOTO [LABEL_J]
    #                     else:
    #                         PROGRAM COMPLETE

    R1 = 10550400
    R2 = 10551287

    # Rewrite again, cleaning up some more.

    # LABEL D

    # R3 = 1   # label D
    # R5 = 1   # label J
    # R1 = R3 * R5  # label H
    # R1 = 1 if R1 == R2 else 0
    # if R1 == 0:
    #     R5 += 1
    # else:
    #     R0 += R3
    #     R5 += 1
    # R1 = 1 if R5 > R2 else 0
    # if R1 == 0:
    #     GOTO [LABEL_H]
    #     ---- keep going to label H while R5 <= R2
    # else:
    #     R3 += 1
    # R1 = 1 if R3 > R2 else 0
    # if R1 == 0:
    #     GOTO [LABEL_J]
    #     ---- keep going to label J while R3 <= R2
    # else:
    #     PROGRAM COMPLETE

    # --------------

    # Once more, as real (ugly) Python code
    # During refactor and cleanup of Python code, realized R1 is exclusively used as a control
    # flow flag. The value of R1 entering this area of the code is irrelavant.

    def _prog():
        # Part 2 starts like this
        R0 = 0
        R2 = 10551287

        # Part 1 starts like this
        # R0 = 0
        # R2 = 887

        # Start main code

        # Label D
        R3 = 1

        # Label J
        while True:
            R5 = 1

            # Label H
            while True:
                if (R3 * R5) == R2:
                    print(f"{R3=} * {R5=} == {R2=}")
                    R0 += R3

                R5 += 1
                if not R5 > R2:
                    continue  # GOTO Label H

                R3 += 1
                if R3 > R2:
                    return R0

                break  # GOTO Label J

    # return _prog()

    # This is summing all the factors of R2 and returning that sum.
    # R3 and R5 are incremented in turn, checked if their product == R2, and if so, R3 is added
    # to R0, the running sum of R3 values which are a factor of R2.

    def _get_all_divisors_of(n):
        if n == 1:
            return [1]

        if n == 2:
            return [1, 2]

        divisors = set()
        for i in range(1, int(ceil(sqrt(n))) + 1):
            if n % i == 0:
                divisors.add(i)
                divisors.add(n / i)

        return list(divisors)

    return int(sum(_get_all_divisors_of(10551287)))


# ----------------------------------------------------------------------------------------------


def run(input_file):
    raw_program = get_input(input_file)

    part_one(raw_program)
    part_two(raw_program)

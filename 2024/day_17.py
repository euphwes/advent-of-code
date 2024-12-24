from util.decorators import aoc_output_formatter
from util.input import get_input

from .computer import Computer

DAY = 17
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    computer = Computer(
        program=[2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0],
        initial_registers={"A": 66752888, "B": 0, "C": 0},
    )

    return ",".join([str(n) for n in computer.execute()])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    target_program = [2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0]
    target_length = len(target_program)

    # Program:
    # 2,4
    # 1,7
    # 7,5
    # 1,7
    # 0,3
    # 4,1
    # 5,5
    # 3,0

    # ---------
    # add assembly instructions

    # 2,4 (BST) B = A % 8      || take lower 3 bits of A and store in B
    # 1,7 (BXL) B = B ^ 7      || 7 in binary is 111, so toggle the lower 3 bits of B
    # 7,5 (CDV) C = A // (2^B) || divide A by 2^B and store in C
    # 1,7 (BXL) B = B ^ 7      || toggle the lower 3 bits of B again
    # 0,3 (ADV) A = A // 8     || divide A by 8 and store in A
    # 4,1 (BXC) B = B ^ C      || B = B ^ C
    # 5,5 (OUT) output (B % 8) || output the lower 3 bits of B
    # 3,0 (JNZ) if A != 0, jump to 0

    # ------------
    #
    # while A != 0:
    #   B = A % 8      # B is the lowest 3 bits of A
    #   B = B ^ 7      # toggle the lowest 3 bits of B
    #
    #   C = A // 2^B   # C = A // 2^B  (bit shift right by B)
    #   B = B ^ 7      # toggle the lowest 3 bits of B again
    #
    #   A = A // 8     # bit shift right by 3 bits
    #   B = B ^ C      # B = B XOR C, aka toggle some bits of B based on C
    #   output B % 8   # output the lowest 3 bits of B

    def _debug(a):
        a_in_binary = bin(a)[2:]
        print()
        print(f"A: {a} (binary: {a_in_binary})")
        output = []
        while True:
            b = a % 8
            b ^= 7
            c = a // (2**b)
            b ^= 7
            a //= 8
            b ^= c
            output.append(b % 8)
            if a == 0:
                break
        # assert len(output) == target_length
        by_program = ",".join([str(n) for n in output])
        print(f"Output: {by_program}")
        return by_program

    _debug(int("111100010001000101010111010100110010110011011010", 2))
    # this is 265056781806810, which gives us
    # 4,2,0,5,3,5,6,[7,0,3,4,1,5,5,3,0]


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

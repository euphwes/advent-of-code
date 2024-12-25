from util.decorators import aoc_output_formatter
from util.input import get_input

from .computer import Computer

DAY = 17
YEAR = 2024

PART_ONE_DESCRIPTION = "output of the program with the given starting register A"
PART_ONE_ANSWER = "2,0,4,2,7,0,1,0,3"

PART_TWO_DESCRIPTION = "smallest starting value for register A that produces a quine"
PART_TWO_ANSWER = 265601188299675


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return ",".join(
        [
            str(n)
            for n in Computer(
                program=[2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0],
                initial_registers={
                    "A": 66752888,
                    "B": 0,
                    "C": 0,
                },
            ).execute()
        ],
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    target_program = [2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0]

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

    def _run(a):
        output = []
        while a:
            b = a % 8
            b = b ^ 7
            c = a // (2**b)
            b = b ^ 7
            a = a // 8
            b = b ^ c
            output.append(b % 8)
        return output

    def _solve_digit(n, candidates):
        possibilities_for_n_digits = []

        for answer in candidates:
            for i in range(8):
                candidate = bin(answer)[2:] + "000"
                candidate = int(candidate, 2) + i
                output = _run(candidate)
                if output == target_program[-1 * n :]:
                    possibilities_for_n_digits.append(candidate)

        if n == 16:
            return possibilities_for_n_digits

        return _solve_digit(n + 1, possibilities_for_n_digits)

    solution = min(_solve_digit(1, [0]))
    if (
        Computer(
            program=target_program,
            initial_registers={"A": solution, "B": 0, "C": 0},
        ).execute()
        != target_program
    ):
        msg = "Sanity check failed"
        raise ValueError(msg)
    return solution


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

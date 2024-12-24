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


def _compare_output(output: list[int], target_program: list[int]) -> int:
    target_len = len([2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0])
    output_len = len(output)
    if output_len < target_len:
        return -1
    if output_len > target_len:
        return 1
    return 0


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    target_program = [2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0]
    # target_program = [0, 3, 5, 4, 3, 0]

    def _run(register_a):
        return Computer(
            program=target_program,
            initial_registers={
                "A": register_a,
                "B": 0,
                "C": 0,
            },
        ).execute()

    # Program: 2,4,1,7,7,5,1,7,0,3,4,1,5,5,3,0
    # 2100000000
    # for i in int_stream():
    #     computer = Computer(
    #         program=target_program,
    #         initial_registers={
    #             "A": i,
    #             "B": 0,
    #             "C": 0,
    #         },
    #     )
    #     raw_output = computer.execute()
    #     print(f"i={i}, output={','.join([str(n) for n in raw_output])}")
    #     if raw_output == target_program:
    #         return i

    sa = 1
    while True:
        output = _run(sa)
        if _compare_output(output, target_program) == -1:
            sa *= 10
        elif _compare_output(output, target_program) == 1:
            sa /= 5
        else:
            break
    sa = int(sa)

    print(f"right order of magnitude with register A = {sa}")

    # increment = sa // 100000
    # while True:
    #     str_output = ",".join([str(n) for n in _run(sa)])
    #     # if not str_output.endswith("5,1,7,0,3,4,1,5,5,3,0"):
    #     # if not str_output.endswith("1,5,5,3,0"):  # with inc = sa // 100
    #     # if not str_output.endswith("3,4,1,5,5,3,0"):  # with inc = sa // 10000 ** this works
    #     if not str_output.endswith(
    #         "0,3,4,1,5,5,3,0"
    #     ):  # with inc = sa // 100000 ** this works in 90s
    #         sa += increment
    #         continue
    #     break

    # right order of magnitude with register A = 100000000000000
    # startswith "0,3,4,1,5,5,3,0"
    # maybe getting closer? sa=2120454000000000 and str_output='0,7,5,1,5,2,6,6,1,0,3,4,1,5,5,3,0'

    sa = 2120454000000000
    increment = sa // 100_000_000

    while True:
        str_output = ",".join([str(n) for n in _run(sa)])
        if not str_output.endswith(
            "7,0,3,4,1,5,5,3,0",  # increment = sa // 100_000_000
        ):
            sa += increment
            continue
        break

    print(f"\nmaybe getting closer? {sa=}, {increment=} and {str_output=}")

    # sa = 2120454000000000
    # increment = sa // 100_000_000  --> 21204540
    # --->
    # sa=2120454254454480
    # str_output='5,4,2,0,5,3,5,6,7,0,3,4,1,5,5,3,0'
    #               need lower?   *

    sa = 2120454000000000
    increment = sa // 1_000_000_000

    while True:
        str_output = ",".join([str(n) for n in _run(sa)])
        print(f"{sa=}, {str_output=}")
        if str_output.endswith(
            "1,7,0,3,4,1,5,5,3,0",
        ):
            break
        sa += increment
        break
        continue

    print(f"\nmaybe getting closer? {sa=}, {increment=} and {str_output=}")
    return


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

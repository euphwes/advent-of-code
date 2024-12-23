from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

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
    # Program: 2,4,1,7,7,5,1,7,0,3,4,1,5,5,3,0
    # 2100000000
    f = []
    for i in int_stream(end=100):
        computer = Computer(
            program=[2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0],
            initial_registers={
                "A": i,
                "B": 0,
                "C": 0,
            },
        )
        raw_output = [str(n) for n in computer.execute()]
        output = ",".join(raw_output)
        output_b8_to_b10 = int("".join(raw_output), 8)
        f.append(str(output_b8_to_b10))
        # if i % 100000 == 0:
        # print(f"\nTrying i={i}, output={output}, b8={output_b8_to_b10}")
        # print(rf"i={i}, b8={output_b8_to_b10}")
        if output == "2,4,1,7,7,5,1,7,0,3,4,1,5,5,3,0":
            return i
    print(",".join(f))
    raise RuntimeError("No solution found")


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

from collections import defaultdict
from collections.abc import Generator

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 16
YEAR = 2019

PART_ONE_DESCRIPTION = "first 8 digits of signal after 100 FFTs"
PART_ONE_ANSWER = "59281788"

PART_TWO_DESCRIPTION = "8-digit message at <offset> in signal repeated 10,000 times"
PART_TWO_ANSWER = "96062868"


def _fft_pattern(digit_number: int) -> Generator[int]:
    while True:
        for _ in range(digit_number):
            yield 1

        for _ in range(digit_number):
            yield 0

        for _ in range(digit_number):
            yield -1

        for _ in range(digit_number):
            yield 0


def _fft(input_signal: list[int]) -> list[int]:
    output_signal = []

    for digit_ix in range(len(input_signal)):
        pattern_generator = _fft_pattern(digit_number=digit_ix + 1)
        ones_digit_of_sum = (
            abs(sum(next(pattern_generator) * digit for digit in input_signal[digit_ix:])) % 10
        )
        output_signal.append(ones_digit_of_sum)

    return output_signal


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    signal = [int(n) for n in raw_input[0]]
    for _ in range(100):
        signal = _fft(signal)

    return "".join([str(n) for n in signal[:8]])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    signal = [int(n) for n in raw_input[0]]
    offset = int("".join([str(n) for n in signal[:7]]))

    true_signal = []
    for _ in range(10_000):
        true_signal.extend(signal)

    signal_size = len(true_signal)

    # Because of the how the "mask" pattern is applied (0, 1, 0, -1) each repeated
    # "digit number" times against the previous phase's signal, any digit in the back
    # half of a signal is just the sum (mod 10) of all digits in the previous phase
    # in the 2nd half of the signal, up to that same digit number.

    cumulative_sums_by_phase: dict[int, list[int]] = defaultdict(list)

    for ix in reversed(range(offset, signal_size)):
        if ix == signal_size - 1:
            cumulative_sums_by_phase[1].append(true_signal[ix])
        else:
            cumulative_sums_by_phase[1].append(
                (true_signal[ix] + cumulative_sums_by_phase[1][-1]) % 10,
            )

    for phase in range(2, 100 + 1):
        for j, ix in enumerate(reversed(range(offset, signal_size))):
            if ix == signal_size - 1:
                cumulative_sums_by_phase[phase].append(true_signal[ix])
            else:
                cumulative_sums_by_phase[phase].append(
                    (
                        cumulative_sums_by_phase[phase - 1][j]
                        + cumulative_sums_by_phase[phase][-1]
                    )
                    % 10,
                )

    return "".join(str(n) for n in list(reversed(cumulative_sums_by_phase[100]))[:8])


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

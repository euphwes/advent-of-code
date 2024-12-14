from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 22
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _mix(val: int, secret: int) -> int:
    return val ^ secret


def _prune(val: int) -> int:
    return val % 16777216


def _next_secret(secret: int) -> int:
    step1 = _prune(_mix(secret * 64, secret))
    step2 = _prune(_mix(step1 // 32, step1))
    return _prune(_mix(step2 * 2048, step2))


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    sums = 0
    for secret in raw_input:
        secret = int(secret)
        for _ in range(2000):
            secret = _next_secret(secret)
        sums += secret
    return sums


def _get_changes(secrets: list[int]) -> dict[tuple[int], int]:
    ones_digits = [int(str(secret)[-1]) for secret in secrets]
    deltas = [ones_digits[i] - ones_digits[i - 1] for i in range(1, len(ones_digits))]

    sale_options = dict()
    for i in range(3, len(ones_digits) - 1):
        pattern = tuple(deltas[i - 3 : i + 1])
        if pattern not in sale_options:
            sale_options[pattern] = ones_digits[i + 1]

    return sale_options


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    sale_options = defaultdict(list)

    for secret in raw_input:
        secret = int(secret)
        buyer = [secret]
        for _ in range(2000):
            secret = _next_secret(secret)
            buyer.append(secret)

        options = _get_changes(buyer)
        for pattern, sale_price in options.items():
            sale_options[pattern].append(sale_price)

    return max(sum(prices) for prices in sale_options.values())


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

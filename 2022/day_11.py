from functools import reduce

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 11
YEAR = 2022

PART_ONE_DESCRIPTION = "monkey business over 20 rounds"
PART_ONE_ANSWER = 72884

PART_TWO_DESCRIPTION = "monkey business over 10,000 rounds with big worry"
PART_TWO_ANSWER = 15310845153


class Monkey:
    def __init__(self, items, operation, test_value, true_monkey, false_monkey):
        self.items = items
        self.operation = operation
        self.test_value = test_value
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspection_count = 0

    def inspect_items(self, monkeys, divisor_lcm, is_part_two=False):
        """Inspect all of this monkey's items, update worry level, and then throw the item to
        another monkey based on this monkey's rules."""

        self.inspection_count += len(self.items)

        while self.items:
            item = self.items.pop(0)

            # Figure out by .what value the item's worry is being updated
            # Either "old" (meaning the item's worry value itself), or some other literal int.
            raw_value = self.operation[1]
            update_value = int(raw_value) if raw_value != "old" else item

            # Update the item's worry value either by adding or multiplying by the update value.
            operand = self.operation[0]
            item = item + update_value if operand == "+" else item * update_value

            # In part two, we don't update the item's worry value by dividing by 3...
            throw_me = int(item / 3) if not is_part_two else item

            # ... but we can preserve the worry value's divisibility by all the monkeys' test
            # values by taking the worry value mod the LCM (lowest common multiple) of all test
            # values.This will keep the worry value from becoming unresonably large.
            throw_me = throw_me % divisor_lcm

            # Figure out which monkey will catch this item based on whether this monkey's
            # divisibility check passes.
            divisibility_check_passed = throw_me % self.test_value == 0
            recipient_monkey = (
                self.true_monkey if divisibility_check_passed else self.false_monkey
            )

            monkeys[recipient_monkey].items.append(throw_me)


def _parse_monkeys(monkey_info):
    """Parse the monkeys out of the problem input, and return a list of Monkey instances with
    their starting items."""

    monkeys = list()

    while monkey_info:
        info, monkey_info = monkey_info[:7], monkey_info[7:]
        items = [int(n) for n in info[1].replace("  Starting items: ", "").split(", ")]
        operation = info[2].replace("  Operation: new = old ", "").split()
        test_value = int(info[3].split()[-1])
        true_monkey = int(info[4].split()[-1])
        false_monkey = int(info[5].split()[-1])

        monkey = Monkey(items, operation, test_value, true_monkey, false_monkey)
        monkeys.append(monkey)

    return monkeys


def _run_monkeys_for_n_rounds(monkeys, n, is_part_two):
    """Runs `n` rounds of monkeys inspecting their items and tossing them around."""

    # Calculate lowest common multiple of all monkeys' divisibility test values.
    # Since these are all prime
    divisor_lcm = reduce(lambda x, y: x * y, [m.test_value for m in monkeys], 1)

    for _ in range(n):
        for monkey in monkeys:
            monkey.inspect_items(monkeys, divisor_lcm, is_part_two=is_part_two)

    return monkeys


def _get_monkey_business(monkeys):
    """Returns the total monkey business, which is the product of the number of item inspections
    by the two monkeys with the highest number of inspections."""

    monkeys.sort(key=lambda m: m.inspection_count)
    return monkeys[-1].inspection_count * monkeys[-2].inspection_count


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(monkey_info):
    monkeys = _parse_monkeys(monkey_info)
    monkeys = _run_monkeys_for_n_rounds(monkeys, 20, is_part_two=False)
    return _get_monkey_business(monkeys)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(monkey_info):
    monkeys = _parse_monkeys(monkey_info)
    monkeys = _run_monkeys_for_n_rounds(monkeys, 10_000, is_part_two=True)
    return _get_monkey_business(monkeys)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    monkey_info = get_input(input_file)

    part_one(monkey_info)
    part_two(monkey_info)

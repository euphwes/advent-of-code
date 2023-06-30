from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 10
YEAR = 2016

PART_ONE_DESCRIPTION = "bot number which compared the target microchips"
PART_ONE_ANSWER = 118

PART_TWO_DESCRIPTION = "product of the chip values in outputs 1-3"
PART_TWO_ANSWER = 143153


def _evaluate_robots(instructions, stop_predicate):
    """Keep iterating through the instructions, evaluating the state of each robot and which
    microchips it contains. After evaluating each instruction, check the stop predicate return
    the desired value when the stop predicate is satisfied."""

    def _parse_give_step(step):
        """Parse the step where a donor robot gives its microchips to 2 recipients."""
        donor_bot, recipient_info = step.split(" gives ")
        split_recipients = recipient_info.split(" and ")
        low_recipient = split_recipients[0].replace("low to ", "")
        high_recipient = split_recipients[1].replace("high to ", "")
        return donor_bot, low_recipient, high_recipient

    def _parse_start_step(step):
        """Parse the step where a robot starts with a particular microchip value."""
        value, recipient = step.split(" goes to ")
        value = int(value.replace("value ", ""))
        return value, recipient

    # Address robots/outputs by name, they hold lists of microchips
    robots = defaultdict(list)

    instructions_iter = iter(instructions)
    while True:

        # If the stop predicate has been satisfied, return the value it returns
        if (return_val := stop_predicate(robots)) is not None:
            return return_val

        # Pop the next instruction off the queue.
        step = next(instructions_iter)

        if "gives" in step:
            # If it's a "give" step, get the donor and recipients.
            donor_bot, low_recipient, high_recipient = _parse_give_step(step)

            # Check if we're able to evaluate this step yet. If the donor robot doesn't have two
            # microchips yet, we can't evaluate it. Take this step and append it to the end of
            # the instructions, and we'll try to append it next time it comes around.
            donor_bot_microchips = robots[donor_bot]
            if not len(donor_bot_microchips) == 2:
                instructions.append(step)
                continue

            # Give the low recipient the donor robot's low-valued microchip, and the high
            # recipient the donor robot's high-valued microchip.
            robots[low_recipient].append(min(donor_bot_microchips))
            robots[high_recipient].append(max(donor_bot_microchips))

        else:
            # Give the recipient robot the specified microchip value to start.
            value, recipient = _parse_start_step(step)
            robots[recipient].append(value)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions):
    def stop_and_return(robots):
        """Stop evaluating if we find the robot with microchips #17 and #61, and return the
        robot number which is holding those chips."""

        for robot, chips in robots.items():
            if all(val in chips for val in [17, 61]):
                return int(robot.replace("bot ", ""))

        # If we don't find that robot, we need to keep evaluating.
        return None

    return _evaluate_robots(instructions, stop_and_return)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(instructions):
    def stop_and_return(robots):
        """Stop evaluating if we find that output 0, output 1, and output 2 all contain
        microchips, and return the product of the values of those microchips."""

        outputs = ["output 0", "output 1", "output 2"]
        if all(len(robots[output]) == 1 for output in outputs):
            return robots["output 0"][0] * robots["output 1"][0] * robots["output 2"][0]

        # If those outputs don't all contain values yet, we need to keep evaluating.
        return None

    return _evaluate_robots(instructions, stop_and_return)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    instructions = get_input(input_file)
    part_one(instructions)

    instructions = get_input(input_file)
    part_two(instructions)

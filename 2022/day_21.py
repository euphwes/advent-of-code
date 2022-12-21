from copy import copy

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 21
YEAR = 2022

PART_ONE_DESCRIPTION = "monkey named root yells"
PART_ONE_ANSWER = 66174565793494

PART_TWO_DESCRIPTION = "you (humn) need to yell"
PART_TWO_ANSWER = 3327575724809


def _get_monkey_values(monkey_info, is_part_two=False):
    """Evaluates the input file to build up a dictionary of monkey to the value they yell."""

    monkeys = dict()

    last_unevaluated_size = None

    # While we still have unevaluated monkey info...
    while monkey_info:

        # In part 2, we want to return the monkey info dict when we no longer are able to
        # calculate any monkeys because we don't know the value for 'humn'.
        unevaluated_size = len(monkey_info)
        if is_part_two:
            if unevaluated_size == last_unevaluated_size:
                return monkeys
            else:
                last_unevaluated_size = unevaluated_size

        # Hold monkeys we can't evaluate yet because we don't know one of their parts.
        unevaluated_monkeys = list()

        # Iterate through every (unevaluated) line...
        for line in monkey_info:
            monkey, value = line.split(": ")

            # In part 2, the value after 'humn' is ignored because WE are human and the problem
            # is to figure out what value of humn satisfies the condition.
            if is_part_two and monkey == "humn":
                continue

            # If the value that monkey holds is just an integer, set it in the map and carry on.
            try:
                monkeys[monkey] = int(value)
                continue
            except:
                pass

            # Otherwise the value that monkey holds is the combo of two other monkeys's values
            # with some operand applied. If we don't know both component monkeys' values, we
            # can't calculate this monkey's value yet, so add it to the list of stuff to be
            # evaluated next pass.
            part1, op, part2 = value.split()

            if not all(component in monkeys.keys() for component in [part1, part2]):
                unevaluated_monkeys.append(line)
                continue

            # If we do know all the component pieces, calculate this monkey's value and set it.
            monkey1, monkey2 = monkeys[part1], monkeys[part2]
            if op == "*":
                monkeys[monkey] = int(monkey1 * monkey2)
            elif op == "/":
                monkeys[monkey] = int(monkey1 / monkey2)
            elif op == "+":
                monkeys[monkey] = int(monkey1 + monkey2)
            elif op == "-":
                monkeys[monkey] = int(monkey1 - monkey2)
            else:
                raise ValueError(f"Unknown {op=}")

            # If we're doing part 1 and we know the value for root, return the monkey dict.
            if not is_part_two and "root" in monkeys.keys():
                return monkeys

        # Set the lines we couldn't evaluate yet back to monkey_info so we'll make another pass.
        # Some of these we'll be able to evaluate next time around.
        monkey_info = unevaluated_monkeys

    return monkeys


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(monkey_info):

    return _get_monkey_values(monkey_info)["root"]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(monkey_info):

    # We're going to modify monkey_info inside _get_monkey_values below, but we need an
    # unaltered copy to work through later.
    clean_monkey_info_copy = copy(monkey_info)

    # Get a dict of monkey values we're able to calculate so far, without specifying the value
    # for 'humn'.
    known_monkeys = _get_monkey_values(monkey_info, is_part_two=True)

    # Iterate through the clean monkey info copy, but replace monkey names on the right-hand
    # side with their values if known.
    #
    # Ex:
    #
    # aaaa: 123
    # bbbb: 234
    # cccc: aaaa + bbbb
    # dddd: cccc * eeee
    # eeee: ffff / gggg
    #
    # becomes
    #
    # aaaa: 123
    # bbbb: 234
    # cccc: 357
    # dddd: 357 * eeee
    # eeee: ffff / gggg

    partially_evaluated_monkeys = list()

    for line in clean_monkey_info_copy:
        lhs, rhs = line.split(": ")
        try:
            int(rhs)
            partially_evaluated_monkeys.append(line)
            continue
        except:
            pass

        p1, _, p2 = rhs.split()
        rhs = rhs.replace(p1, str(known_monkeys.get(p1, p1)))
        rhs = rhs.replace(p2, str(known_monkeys.get(p2, p2)))

        partially_evaluated_monkeys.append(f"{lhs}: {rhs}")

    # Build up a new dict of monkey name to their values, except now the right hand side can
    # contain expressions that are partially known (like `eeee + 1234`).

    new_monkey_values = dict()
    for line in partially_evaluated_monkeys:
        lhs, rhs = line.split(": ")
        new_monkey_values[lhs] = rhs

    # Monkey names are always exactly 4 characters long. Below is a helper function which just
    # slides a 4-character window across a string until it finds a 4-character sequence which we
    # identify as a monkey name because it's in a dict of monkey names to values.

    def _scan_for_monkey_name(line):
        for i in range(len(line) - 4):
            chunk = line[i : i + 4]
            if chunk in new_monkey_values.keys():
                return chunk
        raise ValueError(line)

    # Find the expression of the value for the monkey "root", where the right-hand side will
    # contain some expression that's not fully know. Replace the "+" with an "=" because part 2
    # specifies that we're looking for a value which will pass the equality check on the RHS.
    root_line = new_monkey_values["root"]
    root_line = root_line.replace("+", "=")

    # Keep scanning the root line, looking for unevaluated monkey names, and replacing them with
    # a parenthesized version of their own expressions, until we end up with an expression that
    # contains only numbers and the value 'humn'.
    #
    # root: 12345 = 2323 + aaaa
    # 12345 = 2323 + aaaa
    # 12345 = 2323 + (bbbb * 97)
    # 12345 = 2323 + ((cccc - 43) * 97)
    # 12345 = 2323 + (((2 * dddd) - 43) * 97)
    # 12345 = 2323 + (((2 * (humn / 182)) - 43) * 97)
    while True:
        next_replace = _scan_for_monkey_name(root_line)
        root_line = root_line.replace(
            next_replace, f"({new_monkey_values[next_replace]})"
        )
        if "humn" in root_line:
            break

    # Root line now contains an equality expression with only 'humn' as an unknown. Let's do
    # some algebra in code (god this is going to be awful).
    #
    # The right thing would be to parse this into two RPN (reverse polish notation) stack and
    # then pop from one stack and push the opposite operation/value to the other, but I don't
    # want to do that right now. I think I can do this with some gross string replacement and
    # manipulation.

    rhs: str
    rhs, target_value = root_line.split(" = ")
    target_value = int(target_value)

    def _show_math_work(target_value, rhs):
        print(f"\n{target_value} = {rhs}")

    _show_math_work(target_value, rhs)

    operator_converses = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*",
    }

    while rhs != "humn":
        # Parse and do algebra. Simple as that.
        if rhs.startswith("(") and rhs.endswith(")"):
            rhs = rhs[1:-1]

        # This will probably be messy but if we don't have framing parens, we should have a
        # situation where the rhs expression either ends with [<operator>, <integer>] or starts
        # with [<integer>, <operator>]. The rest will be paren-laden garbage but that's ok.
        pieces = rhs.split()

        if pieces[-2] in operator_converses.keys() and not pieces[-1].endswith(")"):
            # We can work on the right side of the expression.

            opposite_operator = operator_converses[pieces[-2]]
            operand = int(pieces[-1])

            # Put back together the remaining rhs
            rhs = " ".join(pieces[:-2])

            if opposite_operator == "*":
                target_value *= operand
            elif opposite_operator == "/":
                target_value /= operand
            elif opposite_operator == "+":
                target_value += operand
            elif opposite_operator == "-":
                target_value -= operand
            else:
                raise ValueError(opposite_operator)

        elif pieces[1] in operator_converses.keys() and not pieces[0].startswith("("):
            # We can work on the left side of the expression.

            operator = pieces[1]
            operand = int(pieces[0])

            # Put back together the remaining rhs
            rhs = " ".join(pieces[2:])

            if operator == "*":
                target_value /= operand
            elif operator == "/":
                raise ValueError("This doesn't happen, it'd be harder to deal with.")
            else:
                if operator == "+":
                    target_value -= operand
                elif operator == "-":
                    # If the operator is "-", it's not the operator that's being subtracted,
                    # it's the remaining of the expression. We still subtract the operand from
                    # both sides, but now the RHS is a negative value, so let's negate both
                    # sides to deal with that.
                    target_value -= operand
                    target_value *= -1
                    # We've already removed the - from the rhs because we stripped the operator
                else:
                    raise ValueError(operator)

                rhs = rhs.strip()
                assert not rhs.startswith("-")

        else:
            raise ValueError("Shouldn't happen, it's probably a parens parsing issue.")

        if rhs.startswith("(") and rhs.endswith(")"):
            rhs = rhs[1:-1]

        target_value = int(target_value)
        _show_math_work(target_value, rhs)

    print()
    return target_value


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = get_input(input_file)

    part_one(stuff)
    part_two(stuff)

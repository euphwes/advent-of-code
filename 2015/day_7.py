from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

DAY = 7
YEAR = 2015

PART_ONE_DESCRIPTION = "signal on wire a"
PART_ONE_ANSWER = 16076

PART_TWO_DESCRIPTION = "signal on wire a"
PART_TWO_ANSWER = 2797


class UnresolvedSignalsException(BaseException):
    pass


__bitwise_operators = {
    "OR": lambda x, y: x | y,
    "AND": lambda x, y: x & y,
    "RSHIFT": lambda x, y: x >> y,
    "LSHIFT": lambda x, y: x << y,
}


def _evaluate(expr, wires):
    """Attempts to evaluate the expression provided, given the signals we already know."""

    # If the expression has one token, it's just a single signal/value
    if len(expr) == 1:
        token = expr[0]
        try:
            # Try to evaluate as an integer and return
            return int(token)
        except ValueError:
            # If it's not an integer, see if it's a signal we already know and return that
            if token in wires.keys():
                return wires[token]
            # If we don't know this signal, raise an exception
            else:
                raise UnresolvedSignalsException()

    # If the expression has two tokens, it must be `NOT <signal>`.
    # Evaluate <signal> and take its complement
    if len(expr) == 2:
        return ~_evaluate([expr[1]], wires)

    # If the expression has three tokens, it must be OR, AND, LSHIFT, or RSHIFT with two
    # operands. Grab and evaluate the operands, then run through the correct operation
    lhs, rhs = _evaluate([expr[0]], wires), _evaluate([expr[2]], wires)
    return __bitwise_operators[expr[1]](lhs, rhs)


def _evaluate_all_signals(connections):
    """Evaluates all signals in the given list of connections."""

    wires = dict()

    # Continuously iterate over the connections, evaluating what we're able to at each pass and
    # then removing that expression from the connections. When the list of connects is empty,
    # we'll break
    while True:
        indices_to_pop = list()
        for i, (lhs, rhs) in enumerate(connections):

            # Try to evaluate the left hand side of the expression. If we're able, store the
            # value of that expression into the signal specified by the right hand side. Then
            # save the index of the current connection so we can remove it from the list once we
            # complete this pass.
            try:
                evaluated_lhs = _evaluate(lhs, wires)
                wires[rhs] = evaluated_lhs
                indices_to_pop.append(i)

            # The left hand side can't be evaluated because we don't know the value of one of
            # its signals yet. Skip and we'll try again next pass.
            except UnresolvedSignalsException:
                pass

        # Remove all connections we evaluated on this last pass
        for i in indices_to_pop[::-1]:
            connections.pop(i)

        # If the connections list is empty, break so we can return the signal values
        if not connections:
            break

    return wires


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(connections):
    wires = _evaluate_all_signals(connections)
    return wires["a"]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(connections):
    wires = _evaluate_all_signals(connections)
    return wires["a"]


# ----------------------------------------------------------------------------------------------


def run(input_file):

    connections = [
        (lhs.split(), rhs.strip()) for lhs, rhs in get_tokenized_input(input_file, "->")
    ]
    signal_a = part_one(connections)

    # Grab the input again, but this time remove the connection that supplies signal `b` and
    # then apply the end result on wire `a` from part 1 to the signal `b` for the next run.
    connections = [
        (lhs.split(), rhs.strip()) for lhs, rhs in get_tokenized_input(input_file, "->")
    ]
    connections = [(lhs, rhs) for (lhs, rhs) in connections if not rhs == "b"]
    connections.append(([signal_a], "b"))
    part_two(connections)

from contextlib import ContextDecorator
from datetime import timedelta
from time import time

AOC_OUTPUT_HEADER = "\nAdvent of Code {year} - Day {day}, part {part}"

MICROS_ELAPSED = "Ran in {} us"
MILLIS_ELAPSED = "Ran in {} ms"
SECONDS_ELAPSED = "Ran in {}.{} s"


def aoc_output_formatter(
    year, day, part, label, ignore_return_val=False, assert_answer=None
):
    """Builds a decorator to format the output for a specific AoC solution function with
    niceties like the current day, which problem part it is, and an optional meaningful label
    for the solution's output.

    The user can optionally choose to ignore the decorated function's return value, which is
    useful if the problem solution is output by some othermeans (like being printed to console),
    not returned by the function."""

    header = AOC_OUTPUT_HEADER.format(year=year, day=day, part=part)
    output_format = "{label}: {value}" if label else "{value}"

    def __aoc_formatter_decorator(fn):
        """The actual decorator applied to the decorated function. Writes a header and builds an
        output string based on the year, day, part, and optional output label passed in
        above."""

        @aocTimer()
        def __fn_wrapper(*args):
            """The decorated function, which is timed using the timer context manager class
            defined below."""

            print(header)
            value = fn(*args)

            # Only print the output (with value returned from decorated function) if we're not
            # ignoring the return value
            if not ignore_return_val:
                print(output_format.format(value=value, label=label))

            if assert_answer is not None:
                if assert_answer != value:
                    err = f"\n{header}"
                    err += f"\n** {value} does not match the expected answer {assert_answer} **"
                    raise Exception(err)
            return value

        # Return the decorated function from the decorator
        return __fn_wrapper

    # Return the decorator we just built
    return __aoc_formatter_decorator


class aocTimer(ContextDecorator):
    """Records the runtime of the decorated function, and prints out a user-friendly
    representation of the elapsed time."""

    def __enter__(self):
        self.start = time()

    def __exit__(self, *args):
        elapsed = time() - self.start
        delta = timedelta(seconds=elapsed)

        seconds = delta.seconds
        millis = delta.microseconds / 1000
        micros = delta.microseconds

        if millis < 1:
            print(MICROS_ELAPSED.format(micros))
        elif seconds < 1:
            print(MILLIS_ELAPSED.format(millis))
        else:
            print(SECONDS_ELAPSED.format(seconds, int(millis)))

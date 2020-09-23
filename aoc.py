import sys
import importlib

#---------------------------------------------------------------------------------------------------

INPUT_PATH  = '{year}/inputs/input_day{day}.txt'
MODULE_NAME = '{year}.day_{day}'

#---------------------------------------------------------------------------------------------------

def __invalid_usage():
    """ Displays a message to the user that they are invoking the script incorrectly."""

    print('\nInvalid usage -- python aoc.py [year] [day]\nex: python aoc.py 2015 1')
    sys.exit(0)


def __get_year_and_day_from_input():
    """ Returns the year and day provided to this script as the command line arguments. """

    if len(sys.argv) != 3:
        __invalid_usage()

    try:
        year_str, day_str = sys.argv[1:]
        year, day = int(year_str), int(day_str)
    except ValueError:
        __invalid_usage()

    return year, day


def __get_module_and_input_path():
    """ Returns the module for the specified year and day, as well as the filepath for the input. """

    year, day = __get_year_and_day_from_input()
    return MODULE_NAME.format(year=year, day=day), INPUT_PATH.format(year=year, day=day)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    module, input_file = __get_module_and_input_path()
    importlib.import_module(module).run(input_file)

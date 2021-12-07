import os
import sys
import importlib

#---------------------------------------------------------------------------------------------------

__INPUT_PATH  = '{year}/inputs/input_day{day}.txt'
__MODULE_NAME = '{year}.day_{day}'

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


def __get_module_and_input_path(year=None, day=None):
    """ Returns the module for the specified year and day, and the path of the input file. """

    if not year and not day:
        year, day = __get_year_and_day_from_input()

    return __MODULE_NAME.format(year=year, day=day), __INPUT_PATH.format(year=year, day=day)


def __get_all_years():
    """ Returns all years I've participated in this Advent of Code repo. """

    years = list()
    for dir in os.listdir('.'):
        try:
            years.append(int(dir))
        except ValueError:
            pass
    years.sort()
    return years


def __get_all_days_for_year(year):
    """ Returns all days I've completed for the specified year. """

    days = list()
    for file in os.listdir(str(year)):
        if not file.startswith('day_'):
            continue
        try:
            cleaned_file = file.replace('day_','').replace('.py', '')
            days.append(int(cleaned_file))
        except ValueError:
            pass
    days.sort()
    return days

#---------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    if 'all' in sys.argv:
        for year in __get_all_years():
            print('\n============\n    {}    \n============'.format(year))
            for day in __get_all_days_for_year(year):
                module, input_file = __get_module_and_input_path(year=year, day=day)
                importlib.import_module(module).run(input_file)

    else:
        module, input_file = __get_module_and_input_path()
        importlib.import_module(module).run(input_file)

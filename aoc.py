import importlib
import os
import sys

from util.decorators import aocTimer

# ----------------------------------------------------------------------------------------------

__INPUT_PATH = "{year}/inputs/input_day{day}.txt"
__MODULE_NAME = "{year}.day_{day}"

# ----------------------------------------------------------------------------------------------


def __invalid_usage():
    """Displays a message to the user that they are invoking the script incorrectly."""
    print("\nInvalid usage -- python aoc.py [year] [day]\nex: python aoc.py 2015 1")


def __get_year_and_day_from_input():
    """Returns the year and day provided to this script as the command line arguments."""
    if len(sys.argv) != 3:
        __invalid_usage()
        sys.exit(0)

    try:
        year_str, day_str = sys.argv[1:]
        year, day = int(year_str), int(day_str)
    except ValueError:
        __invalid_usage()
        sys.exit(0)

    return year, day


def __get_module_and_input_path(year=None, day=None):
    """Returns the module for the specified year and day, and the path of the input file."""
    if not year and not day:
        year, day = __get_year_and_day_from_input()

    return __MODULE_NAME.format(year=year, day=day), __INPUT_PATH.format(
        year=year,
        day=day,
    )


def __get_all_years():
    """Returns all years I've participated in this Advent of Code repo."""
    years = list()
    for dir in os.listdir("."):
        try:
            years.append(int(dir))
        except ValueError:
            pass
    years.sort()
    return years


def __get_all_days_for_year(year):
    """Returns all days I've completed for the specified year."""
    days = list()
    for file in os.listdir(str(year)):
        if not file.startswith("day_"):
            continue
        try:
            cleaned_file = file.replace("day_", "").replace(".py", "")
            days.append(int(cleaned_file))
        except ValueError:
            pass
    days.sort()
    return days


@aocTimer()
def __run_all():
    """Runs all solutions for every year, in order."""
    for year in __get_all_years():
        print(f"\n============\n    {year}    \n============")
        for day in __get_all_days_for_year(year):
            module, input_file = __get_module_and_input_path(year=year, day=day)
            importlib.import_module(module).run(input_file)

    print("\n******** Finished running all completed Advent of Code problems! ********")


def __create_year(year):
    if not os.path.exists(year):
        print(f"Creating directory for year {year}")
        os.mkdir(year)

    if not os.path.exists(f"{year}/inputs"):
        print(f"Creating directory for inputs for year {year}")
        os.mkdir(f"{year}/inputs")

    for day in range(1, 26):
        if not os.path.exists(f"{year}/day_{day}.py"):
            print(f"Creating file for year {year}, day {day}")

            # read day_n_template.py file to memory
            file_contents = ""
            with open("day_n_template.py") as f:
                file_contents = f.read()

            # find the line containing DAY = 'REPLACE_ME' and replace the day number
            file_contents = file_contents.replace('DAY = "REPLACE_ME"', f"DAY = {day}")
            # same for YEAR
            file_contents = file_contents.replace('YEAR = "REPLACE_ME"', f"YEAR = {year}")

            # write the file contents to the new file
            with open(f"{year}/day_{day}.py", "w") as f:
                f.write(file_contents)

        if not os.path.exists(f"{year}/inputs/input_day{day}.txt"):
            print(f"Creating input file for year {year}, day {day}")
            with open(f"{year}/inputs/input_day{day}.txt", "w") as f:
                f.write("")


# ----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if "all" in sys.argv:
        __run_all()

    elif sys.argv[1] == "create":
        year = sys.argv[2]
        __create_year(year)

    else:
        module, input_file = __get_module_and_input_path()
        importlib.import_module(module).run(input_file)

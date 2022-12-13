from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict, Counter
from datetime import datetime

DAY  = 4
YEAR = 2018

PART_ONE_DESCRIPTION = 'strategy 1, ID of guard * favorite minute to sleep'
PART_ONE_ANSWER = 19830

PART_TWO_DESCRIPTION = 'strategy 2, ID of guard * favorite minute to sleep'
PART_TWO_ANSWER = 43695

#---------------------------------------------------------------------------------------------------

def _parse_guard_sleep_log(guard_info):
    """ Parses the problem input and returns a dictionary of guard ID to a list of the minutes they
    were asleep. """

    # Parse the date part of the string and sort by that
    guard_info.sort(key=lambda x: datetime.strptime(x[1:17], '%Y-%m-%d %H:%M'))

    # First line contains a "Guard #X begins shift", find index of "#" for easier parsing later.
    # It also contains a timestamp of same shape as every other line, find index of ":"
    number_ix = guard_info[0].index('#')
    minute_ix = guard_info[0].index(':')

    guard_sleep_log = defaultdict(list)

    for info_line in guard_info:
        if 'begins shift' in info_line:
            short_line = info_line.replace(' begins shift', '')
            guard_id = int(short_line[number_ix+1:])

        elif 'falls asleep' in info_line:
            start_minute = int(info_line[minute_ix+1:minute_ix+3])

        elif 'wakes up' in info_line:
            # For the current guard, add all minutes asleep to his entry
            final_minute = int(info_line[minute_ix+1:minute_ix+3])
            guard_sleep_log[guard_id].extend(list(range(start_minute, final_minute)))

    return guard_sleep_log

            
@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(guard_info):

    guard_sleep_log = _parse_guard_sleep_log(guard_info)

    # Build a list of tuples of (guard_id, list_of_minutes_asleep), sort by the total number
    # of minutes slept.
    guard_sleep_min = [(guard_id, sleeping) for guard_id, sleeping in guard_sleep_log.items()]
    guard_sleep_min.sort(key=lambda x: len(x[1]))

    # For the guard most often asleep, count the frequency he was asleep for any given minute,
    # and then retrieve the minute he was asleep most often.
    minutes_asleep_counter = Counter(guard_sleep_min[-1][1])
    minute_asleep_most_often = minutes_asleep_counter.most_common()[0][0]

    sleepiest_guard_id = guard_sleep_min[-1][0]

    return sleepiest_guard_id * minute_asleep_most_often


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(guard_info):

    guard_sleep_log = _parse_guard_sleep_log(guard_info)

    # Build a list of tuples of (guard_id, list_of_minutes_asleep).
    guard_sleep_min = [(guard_id, sleeping) for guard_id, sleeping in guard_sleep_log.items()]
    guard_sleep_min.sort(key=lambda x: len(x[1]))

    # Hold a list of tuples of (guard_id, minute_slept_most_often, how_many_times_asleep_that_min)
    guard_most_slept_minute = list()
    for guard_id, sleep_minutes in guard_sleep_min:
        most_slept_min, how_many_times = Counter(sleep_minutes).most_common()[0]
        guard_most_slept_minute.append((guard_id, most_slept_min, how_many_times))

    # Sort guards by who was asleep most frequently on the same minute
    guard_most_slept_minute.sort(key=lambda x: x[2])

    sleepiest_guard_id = guard_most_slept_minute[-1][0]
    most_slept_minute = guard_most_slept_minute[-1][1]

    return sleepiest_guard_id * most_slept_minute

#---------------------------------------------------------------------------------------------------

def run(input_file):

    guard_info = get_input(input_file)

    part_one(guard_info)
    part_two(guard_info)

from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def __determine_questions_yes_by_anyone(records):
    """ Turns a record (1 or more lines containing question IDs which somebody answered yes) into a
    single set of question IDs which received a yes answer from anybody in the group. """

    yes_question_ids = set()

    for record in records:
        for q_id in record:
            yes_question_ids.add(q_id)

    return yes_question_ids


def __determine_questions_yes_by_everyone(records):
    """ Turns a record (1 or more lines containing question IDs which somebody answered yes) into a
    single set of question IDs which received a yes answer from everybody in the group. """

    questions_yes_responses = dict()

    for record in records:
        for q_id in record:
            if q_id not in questions_yes_responses:
                questions_yes_responses[q_id] = 1
            else:
                questions_yes_responses[q_id] = questions_yes_responses[q_id] + 1

    group_size = len(records)
    return [q_id for q_id, num_yes in questions_yes_responses.items() if num_yes == group_size]


def __separate_records_in_batch(lines):
    """ Iterate over the lines from the input file, grouping 1 or more lines into individual
    records which are separated by blank lines. """

    records = list()
    record = list()

    for line in lines:
        if line:
            record.append(line)
        else:
            records.append(record)
            record = list()

    if record:
        records.append(record)

    return records

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 6, 1, 'combined yes questions across groups')
def part_one(input_lines):
    questionnaires = __separate_records_in_batch(input_lines)
    yes_questions_by_someone = [__determine_questions_yes_by_anyone(q) for q in questionnaires]

    return sum([len(yes_by_group) for yes_by_group in yes_questions_by_someone])


@aoc_output_formatter(2020, 6, 2, 'combined questions answered yes by everybody in a group')
def part_two(input_lines):
    questionnaires = __separate_records_in_batch(input_lines)
    yes_questions_by_everyone = [__determine_questions_yes_by_everyone(q) for q in questionnaires]

    return sum([len(yes_by_group) for yes_by_group in yes_questions_by_everyone])

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

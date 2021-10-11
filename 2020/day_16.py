from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict

#---------------------------------------------------------------------------------------------------

def __parse_field_ranges(line):
    """ Parse a line of the problem input corresponding to a field name and acceptable values for
    that field. """

    field_name, ranges = line.split(': ')
    range1, range2 = ranges.split(' or ')
    acceptable_values = list()
    for value_range in ranges.split(' or '):
        lower, upper = value_range.split('-')
        acceptable_values.extend(range(int(lower), int(upper)+1))

    return field_name, set(acceptable_values)


def __parse_input(lines):
    """ Parse the problem input into 3 components: a map of ticket fields and their acceptable
    ranges, a representation of your ticket as a list of values, and a list of nearby tickets as
    lists of values. """

    __parse_ticket = lambda line: [int(n) for n in line.split(',')]

    fields = dict()
    nearby_tickets = list()

    mode = 'field ranges'
    for line in [line for line in lines if line]:
        if line in ('your ticket:', 'nearby tickets:'):
            mode = line
            continue
        if mode == 'field ranges':
            field_name, values = __parse_field_ranges(line)
            fields[field_name] = values
        if mode == 'your ticket:':
            your_ticket = __parse_ticket(line)
        if mode == 'nearby tickets:':
            nearby_tickets.append(__parse_ticket(line))

    return fields, your_ticket, nearby_tickets


def __identify_invalid_field_values_in_ticket(ticket, fields):
    """ Returns a list of all invalid fields in a ticket, if they aren't valid values for any
    ticket fields. """

    invalid_values = list()

    for value in ticket:
        valid_somewhere = False
        for _, field_values in fields.items():
            if value in field_values:
                valid_somewhere = True
                break
        if not valid_somewhere:
            invalid_values.append(value)

    return invalid_values


def __determinate_candidate_positions_for_fields(fields, valid_tickets):
    """ Returns a dictionary mapping field name to potential ticket field positions based on the
    tickets we know are valid. """

    field_names = list(fields.keys())
    num_fields  = len(field_names)

    field_pos_candidates = defaultdict(list)

    for field in field_names:
        for i in range(num_fields):
            is_field_candidate = True
            for ticket in valid_tickets:
                if ticket[i] not in fields[field]:
                    is_field_candidate = False
                    break
            if is_field_candidate:
                field_pos_candidates[field].append(i)

    return field_pos_candidates


def __deduce_field_positions(field_pos_candidates):
    """ Takes a mapping of field names to the positions they can possibly be at. Identify at any
    given point in time any fields which do not have ambiguous positions, and remove their position
    from the list of candidate positions of other fields. Continue doing this until only one
    candidate remains for each field, and return this. """

    def __is_completely_reduced(fields):
        for _, v in fields.items():
            if len(v) > 1:
                return False
        return True

    def __identify_unambiguous_positions(fields):
        unambiguous_positions = list()
        for k, v in fields.items():
            if len(v) == 1:
                unambiguous_positions.append((k, v[0]))
        return unambiguous_positions

    while not __is_completely_reduced(field_pos_candidates):
        reductions_this_pass = 0
        for field, pos in __identify_unambiguous_positions(field_pos_candidates):
            for f in field_pos_candidates.keys():
                if f == field:
                    continue
                if pos in field_pos_candidates[f]:
                    reductions_this_pass += 1
                    field_pos_candidates[f].remove(pos)
        if not reductions_this_pass:
            raise ValueError("Can't fully reduce this, something is wrong")

    return {k: v[0] for k, v in field_pos_candidates.items()}

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 16, 1, 'ticket scanning error rate')
def part_one(problem_input):
    fields, your_ticket, nearby_tickets = __parse_input(problem_input)
    error_scanning_rate = 0

    for ticket in nearby_tickets:
        invalid_values = __identify_invalid_field_values_in_ticket(ticket, fields)
        error_scanning_rate += sum(invalid_values)

    return error_scanning_rate


@aoc_output_formatter(2020, 16, 2, "product of your ticket's fields starting with 'departure'")
def part_two(problem_input):
    fields, your_ticket, nearby = __parse_input(problem_input)
    valid_tickets = [t for t in nearby if not __identify_invalid_field_values_in_ticket(t, fields)]

    field_pos_candidates = __determinate_candidate_positions_for_fields(fields, valid_tickets)
    field_positions = __deduce_field_positions(field_pos_candidates)

    answer = 1
    for field, pos in field_positions.items():
        if "departure" not in field:
            continue
        answer *= your_ticket[pos]

    return answer

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

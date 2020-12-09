from util.decorators import aoc_output_formatter
from util.input import get_input

from string import hexdigits

#---------------------------------------------------------------------------------------------------
__REQUIRED_FIELDS = (
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid'
)

def __is_passport_valid(passport):
    """ Determines if a passport is valid by checking if it has all of the required fields. """

    for required_field in __REQUIRED_FIELDS:
        if not required_field in passport.keys():
            return False

    return True

#---------------------------------------------------------------------------------------------------

def __get_year_validator(min_year, max_year):
    """ Returns a validator function which vets the supplied value is a 4-digit integer, and falls
    into the specified range. """

    def __validator(value):
        if len(value) != 4:
            return False

        try:
            year = int(value)
        except ValueError:
            return False

        return year in range(min_year, max_year+1)

    return __validator


def __height_validator(value):
    """ Validates a height value. Centimeter values must end in 'cm' and be in the range 150-193,
    inch values must end in 'in', and be in the range 58-76. Any other value is invalid. """

    if value.endswith('cm'):
        height = int(value[:-2])
        return height in range(150, 194)

    if value.endswith('in'):
        height = int(value[:-2])
        return height in range(59, 77)

    return False


__VALID_HEX_DIGITS_LOWER = set(hexdigits.lower())


def __validate_hair_color(value):
    """ Validates a hair color. It must be a hexadecimal value, starting with '#', and containing
    6 lowercase hexadecimal characters. """

    if not value.startswith('#'):
        return False

    color = value[1:]
    if len(color) != 6:
        return False

    for char in color:
        if not char in __VALID_HEX_DIGITS_LOWER:
            return False

    return True


def __validate_passport_id(value):
    """ Validates a passport ID, which must be a 9-digit number including leading zeros. """

    if len(value) != 9:
        return False

    try:
        int(value)
        return True
    except ValueError:
        pass

    return False


__FIELD_VALIDATORS = {
    'byr': __get_year_validator(1920, 2002),
    'iyr': __get_year_validator(2010, 2020),
    'eyr': __get_year_validator(2020, 2030),
    'hgt': __height_validator,
    'hcl': __validate_hair_color,
    'pid': __validate_passport_id,
    'ecl': lambda value: value in ['amb', 'blu', 'brn', 'grn', 'gry', 'hzl', 'oth'],
    'cid': lambda _: True
}


def __is_passport_content_valid(passport):
    """ Checks all the content of the passport. If any field contains an invalid value, the passport
    content is invalid. """

    for key, value in passport.items():
        if not __FIELD_VALIDATORS[key](value):
            return False

    return True

#---------------------------------------------------------------------------------------------------

def __process_passports(records):
    """ Turns a record (1 or more lines containing passport fields) into a dictionary with key/value
    pairs representing a passport. """

    passports = list()
    for record in records:
        passport = dict()
        for line in record:
            for kvp in line.split(' '):
                key, value = kvp.split(':')
                passport[key] = value
        passports.append(passport)

    return passports


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

@aoc_output_formatter(2020, 4, 1, 'number valid passports')
def part_one(input_lines):
    records = __separate_records_in_batch(input_lines)
    passports = __process_passports(records)

    return sum(1 for passport in passports if __is_passport_valid(passport))


@aoc_output_formatter(2020, 4, 2, 'number passports with valid content')
def part_two(input_lines):
    records = __separate_records_in_batch(input_lines)
    passports = __process_passports(records)

    entirely_valid = lambda p: __is_passport_valid(p) and __is_passport_content_valid(p)
    return sum(1 for passport in passports if entirely_valid(passport))

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

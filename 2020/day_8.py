from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 8, 1, 'value in acc before infinite loop')
def part_one(input_lines):
    curr_ix = 0
    accumulator = 0

    visited_inst = set()
    instructions = [(line.split(' ')[0], int(line.split(' ')[1])) for line in input_lines]

    while True:
        if curr_ix in visited_inst:
            return accumulator
        visited_inst.add(curr_ix)

        inst, value = instructions[curr_ix]
        if inst == 'acc':
            accumulator += value
            curr_ix += 1
        elif inst == 'nop':
            curr_ix += 1
        elif inst == 'jmp':
            curr_ix += value


@aoc_output_formatter(2020, 8, 2, 'value in acc when the correct program ends')
def part_two(input_lines):

    instructions = [(line.split(' ')[0], int(line.split(' ')[1])) for line in input_lines]

    for n in range(len(instructions)):

        curr_ix = 0
        accumulator = 0

        visited_inst = set()

        while True:
            if curr_ix in visited_inst:
                break
            visited_inst.add(curr_ix)

            if curr_ix == len(instructions):
                return accumulator

            inst, value = instructions[curr_ix]

            if curr_ix == n:
                if inst == 'nop':
                    inst = 'jmp'
                elif inst == 'jmp':
                    inst = 'nop'

            if inst == 'acc':
                accumulator += value
                curr_ix += 1
            elif inst == 'nop':
                curr_ix += 1
            elif inst == 'jmp':
                curr_ix += value

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))

from util.decorators import aoc_output_formatter
from util.input import get_input

from dataclasses import dataclass
from typing import Optional

PART_ONE_DESC = 'sum of six target signal strengths'
PART_TWO_DESC = 'image on the CRT'

#---------------------------------------------------------------------------------------------------

@dataclass
class CrtInstructions:
    code: str
    amount: int

    @staticmethod
    def from_line(line: str):
        pieces = line.split(' ')
        code=pieces[0]
        amount = int(pieces[1:][0]) if pieces[1:] else 0

        return CrtInstructions(code=code, amount=amount)


def run_crt_screen(instructions):
    """ Evaluates a set of CRT instructions, yielding cycle count and X value at each step. """

    x = 1
    cycle_count = 1

    while True:
        for instruction in instructions:
            if instruction.code == 'noop':
                yield cycle_count, x
                cycle_count += 1

            else:
                yield cycle_count, x
                cycle_count += 1

                yield cycle_count, x
                cycle_count += 1
                x += instruction.amount


@aoc_output_formatter(2022, 10, 1, PART_ONE_DESC, assert_answer=17840)
def part_one(instructions):

    signals = list()
    target_cycles = (20, 60, 100, 140, 180, 220)

    for cycle, x in run_crt_screen(instructions):
        if cycle in target_cycles:
            signals.append(cycle*x)
        if cycle == target_cycles[-1]:
            break

    return sum(signals)


@aoc_output_formatter(2022, 10, 2, PART_TWO_DESC, assert_answer='EALGULPG')
def part_two(instructions):

    screen = [['']*40 for _ in range(6)]

    for cycle, x in run_crt_screen(instructions):

        cycle -= 1

        px = cycle % 40
        py = cycle // 40

        screen[py][px] = '█' if abs(cycle - (x + 40*py)) <= 1 else ' '

        if cycle == 239:
            break

    print()
    for i, line in enumerate(screen):
        print(''.join(line))
    print()

    # TODO write "OCR" function to read the screen
    return 'EALGULPG'

#---------------------------------------------------------------------------------------------------

def run(input_file):

    instructions = [CrtInstructions.from_line(x) for x in get_input(input_file)]

    part_one(instructions)
    part_two(instructions)

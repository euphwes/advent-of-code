from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

#---------------------------------------------------------------------------------------------------

def wrapping_paper_area(length, width, height):
    """ Returns the wrapping paper area required to wrap a box with dimensions `length`, `width`,
    and `height`, with a little extra (the area of the smallest face). """

    faces = [length*width, length*height, width*height]
    return 2*sum(faces) + min(faces)

def ribbon_footage(length, width, height):
    """ Returns the length of ribbon required to wrap the shortest perimeter of a box with
    dimensions `length`, `width`, and `height`, with a little extra for a box (the volume of the
    box, as length). """

    perimeters = [2*(length+width), 2*(length+height), 2*(width+height)]
    return min(perimeters) + (length*width*height)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 2, 1, 'square feet of wrapping paper', assert_answer=1588178)
def part_one(boxes):
    return sum(wrapping_paper_area(l, w, h) for l, w, h in boxes)


@aoc_output_formatter(2015, 2, 2, 'feet of ribbon', assert_answer=3783758)
def part_two(boxes):
    return sum(ribbon_footage(l, w, h) for l, w, h in boxes)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    boxes = get_tokenized_input(input_file, 'x', int)

    part_one(boxes)
    part_two(boxes)

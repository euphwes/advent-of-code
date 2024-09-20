from util.input import get_input
from util.iter import nested_iterable
from util.decorators import aoc_output_formatter


DAY = 8
YEAR = 2019

PART_ONE_DESCRIPTION = "count of 1 * count of 2"
PART_ONE_ANSWER = 2176

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


class LayeredImage:
    """An image built from layers of pixels that are black, white, or
    transparent. When rendered, any transparent pixels show the color of the
    pixel below it."""

    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2

    PIXEL_MAP = {BLACK: "█", WHITE: " "}

    def __init__(self, pixels, width, height, padding=2):
        self.width = width
        self.height = height
        self.padding = padding

        layers = self._build_layers(pixels)
        self.image = self._build_image(layers)

    def _build_layers(self, pixels):
        """Iterates over the raw flat list of pixel values, building them into
        image layers. Each layer is a 2D array with dimensions w x h.

        [0,0,2,2,1,1,2,2,1,1,0,0] for 2x2 image -->

        [[0,0],  [[1,1],  [[1,1],
         [2,2]]   [2,2]]   [0,0]]"""

        w = self.width
        h = self.height

        layers = list()
        for chunk in [pixels[i : i + w * h] for i in range(0, len(pixels), w * h)]:
            layers.append([chunk[i : i + w] for i in range(0, len(chunk), w)])

        return layers

    def _build_image(self, layers):
        """Builds the final image in a single 2D array. For each point (x,y) in the image,
        determine the color of the pixel at that coordinate by finding the first non-transparent
        pixel at that coordinate starting from the top layer and working down."""

        w = self.width
        h = self.height

        image = [[-1 for i in range(w)] for j in range(h)]

        for x, y in nested_iterable(range(w), range(h)):
            for layer in layers:
                if layer[y][x] == LayeredImage.TRANSPARENT:
                    continue
                else:
                    image[y][x] = layer[y][x]
                    break

        return image

    def render(self):
        """Returns a string representation of the image, with `█` and space characters to
        represent black and white pixels."""

        pad = self.padding
        width = self.width
        black_px = LayeredImage.PIXEL_MAP[LayeredImage.BLACK]

        # Extra rows to pad the top/bottom of the image, which are themselves the correct
        # padded witdth.
        extra_rows = ((black_px * (width + 2 * pad)) + "\n") * pad

        # Padding for the left and right of each row of the image itself.
        row_padding = black_px * pad

        # For each row in the image, map the pixel to the correct character and pad left and
        # right, ending in a newline to move to the next row.
        ret = ""
        for row in self.image:
            row_str = "".join([LayeredImage.PIXEL_MAP[px] for px in row])
            ret += row_padding + row_str + row_padding + "\n"

        return (extra_rows + ret + extra_rows).strip()


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(pixels):
    # Chunk the pixels into layers of 25*6 pixels each.
    # For each layer, note its index and the number of zeros it contains
    layers = [pixels[i : i + (25 * 6)] for i in range(0, len(pixels), 25 * 6)]
    layer_zero_counts = [(i, layers[i].count(0)) for i in range(len(layers))]

    # Get the index of the layer with the fewest zeroes
    i = min(layer_zero_counts, key=lambda x: x[1])[0]

    return layers[i].count(1) * layers[i].count(2)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION)
def part_two(pixels):
    print(LayeredImage(pixels, 25, 6).render())


# ----------------------------------------------------------------------------------------------


def run(input_file):
    problem_input = [int(c) for c in get_input(input_file)[0]]

    part_one(problem_input)
    part_two(problem_input)

from dataclasses import dataclass

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 10
YEAR = 2018


@dataclass
class Particle:
    x: int
    y: int
    dx: int
    dy: int

    @staticmethod
    def from_line(line):
        """Parses and returns a Particle instance out of a line from the problem input."""

        # position=<-6, 10> velocity=< 2, -2>
        pos_half, vel_half = line.split("> ")

        # pos_half: position=<-6, 10
        pos_half = pos_half.replace("position=<", "")
        x, y = (int(n) for n in pos_half.split(","))

        # vel_half: velocity=< 2, -2>
        vel_half = vel_half.replace("velocity=<", "")[:-1]
        dx, dy = (int(n) for n in vel_half.split(","))

        return Particle(x=x, y=y, dx=dx, dy=dy)

    @property
    def coord(self):
        return (self.x, self.y)

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def reverse(self):
        self.x -= self.dx
        self.y -= self.dy


def _get_bounding_region(particles):
    """For a given group of particles, returns the min and max x/y values defining the smallest
    rectangle which bounds all the particles."""

    all_x = [p.x for p in particles]
    all_y = [p.y for p in particles]

    return min(all_x), max(all_x), min(all_y), max(all_y)


def _get_region_size(particles):
    """For a given group of particles, return the size of the bounding rectangle around them."""

    min_x, max_x, min_y, max_y = _get_bounding_region(particles)
    return (max_x - min_x) * (max_y - min_y)


def _render(elapsed_seconds, particles):
    """Render the particles within the smallest bounding rectangle that contains them, with a
    little extra blurb that says at what timestamp this occurs."""

    particle_positions = {p.coord for p in particles}
    min_x, max_x, min_y, max_y = _get_bounding_region(particles)

    print(f"\nAfter {elapsed_seconds} seconds...\n")

    for y in range(min_y, max_y + 1):
        # Left-padding each line so it doesn't start at the terminal edge and is easier to read
        line = "  "
        for x in range(min_x, max_x + 1):
            cell = "█" if (x, y) in particle_positions else " "
            line += cell
        print(line)
    print()


@aoc_output_formatter(YEAR, DAY, "both parts", None, ignore_return_val=True)
def part_one(raw_particles):

    particles = [Particle.from_line(line) for line in raw_particles]
    prev_region_size = None

    # For each timestep...
    for i in int_stream():

        # Move all the particles via their velocity
        for p in particles:
            p.move()

        # Get the region size (the area of the smallest bounding rectangle around the particles)
        region_size = _get_region_size(particles)

        # Intuitively, the size of the region containing the particles will get smaller as they
        # all fly in towards each other, and will be at a minimum when the text is visible. Keep
        # track of the size of the regions and once we see that the region is growing again, we
        # know the particles are moving back apart. Move them back one timestep and then render
        # the particles.
        if prev_region_size is not None and region_size > prev_region_size:
            for p in particles:
                p.reverse()
            _render(i, particles)
            return

        prev_region_size = region_size


# ----------------------------------------------------------------------------------------------


def run(input_file):

    raw_particles = get_input(input_file)
    part_one(raw_particles)

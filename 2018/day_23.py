from heapq import heappop, heappush
from dataclasses import dataclass
from typing import Tuple, List, Generator
from util.algs import manhattan_distance_3d
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import min_and_max, triple_iterable

DAY = 23
YEAR = 2018

PART_ONE_DESCRIPTION = "number of nanobots in range of the bot with the largest radius"
PART_ONE_ANSWER = 730

PART_TWO_DESCRIPTION = "distance from origin of the point in range of the most bots"
PART_TWO_ANSWER = 48202279


@dataclass(frozen=True)
class Nanobot:
    """
    Represents a nanobot which has a particular (x,y,z) location in 3D space,
    and a radius around itself where its signals can reach.
    """

    x: int
    y: int
    z: int
    radius: int

    @property
    def coord(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    @property
    def vertices(self) -> Generator[Tuple[int, int, int], None, None]:
        """
        Because the bot exists in a grid and signal radius defines Manhattan distance
        which the bot can reach, the space that can be reached within the bot's signal
        radius is a 3D sort of diamond shape.

        This yields the "vertices" of the field of influence of this bot, basically just
        +/- the radius in all cardinal directions, from the point which this bot occupies.
        """

        yield (self.x - self.radius, self.y, self.z)
        yield (self.x + self.radius, self.y, self.z)
        yield (self.x, self.y - self.radius, self.z)
        yield (self.x, self.y + self.radius, self.z)
        yield (self.x, self.y, self.z - self.radius)
        yield (self.x, self.y, self.z + self.radius)

    def is_within_range(self, other: "Nanobot") -> bool:
        """
        Returns whether this Nanobot and another bot are within range of each other.
        """

        largest_radius = max([self.radius, other.radius])
        return manhattan_distance_3d(self.coord, other.coord) <= largest_radius

    @staticmethod
    def from_line(line) -> "Nanobot":
        """
        Eg: pos=<23,-47,10>, r=6
        --> Nanobot(x=23, y=-47, z=10, radius=6)
        """

        acceptable_chars = set("0123456789-,")
        raw_line = "".join(c for c in line if c in acceptable_chars)
        x, y, z, radius = tuple(int(n) for n in raw_line.split(","))
        return Nanobot(x=x, y=y, z=z, radius=radius)

    @staticmethod
    def from_lines(lines) -> List["Nanobot"]:
        return [Nanobot.from_line(line) for line in lines]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    nanobots = Nanobot.from_lines(stuff)
    largest_bot = max(nanobots, key=lambda bot: bot.radius)
    return sum(1 for bot in nanobots if bot.is_within_range(largest_bot))


@dataclass
class SearchBox:
    """
    Represents a 3D box in space, with which a Nanobot may "intersect". That is, the box and
    the "range" of the Nanobot may occupy some of the same space.
    """

    # The upper and lower planes of the box on the x, y, and z axes.
    x_bounds: Tuple[int, int]
    y_bounds: Tuple[int, int]
    z_bounds: Tuple[int, int]

    @property
    def size(self):
        """
        The box is a cube, and so we can represent the size of it as a single integer that
        is the length of one side.
        """
        return self.x_bounds[1] - self.x_bounds[0]

    @property
    def corners(self) -> Generator[Tuple[int, int, int], None, None]:
        """
        Yields the coordinates of the 8 corners of the box.
        """
        yield from triple_iterable(self.x_bounds, self.y_bounds, self.z_bounds)

    def contains(self, point: Tuple[int, int, int]) -> bool:
        """
        Returns whether the provided point is contained within the box.
        """
        px, py, pz = point
        return (
            px >= self.x_bounds[0]
            and px <= self.x_bounds[1]
            and py >= self.y_bounds[0]
            and py <= self.y_bounds[1]
            and pz >= self.z_bounds[0]
            and pz <= self.z_bounds[1]
        )

    def get_num_intersecting_bots(self, bots: List[Nanobot]) -> int:
        """
        Given a list of Nanobots, returns a count of how many of them "intersect" the box by
        the box occupying some space which the radius of the Nanobot also occupies.
        """
        count = 0

        for bot in bots:
            determined_intersection = False
            # Bot and box can intersect in 2 different ways.

            # If a corner of the box is inside the radius of the bot...
            for corner in self.corners:
                if manhattan_distance_3d(corner, bot.coord) <= bot.radius:
                    count += 1
                    determined_intersection = True
                    break

            if determined_intersection:
                continue

            # ... or if a vertex of a bot is inside the bounds of the box.
            for vertex in bot.vertices:
                if self.contains(vertex):
                    count += 1
                    break

        return count

    def get_smaller_boxes(self) -> List["SearchBox"]:
        """
        Divide this box in half along all 3 axes, returning a list of the 8 boxes that makes.
        """
        x_range = self.x_bounds[1] - self.x_bounds[0]
        y_range = self.y_bounds[1] - self.y_bounds[0]
        z_range = self.z_bounds[1] - self.z_bounds[0]

        x_half = x_range // 2
        y_half = y_range // 2
        z_half = z_range // 2

        x_lower = (self.x_bounds[0], self.x_bounds[0] + x_half)
        x_upper = (self.x_bounds[0] + x_half + 1, self.x_bounds[1])
        y_lower = (self.y_bounds[0], self.y_bounds[0] + y_half)
        y_upper = (self.y_bounds[0] + y_half + 1, self.y_bounds[1])
        z_lower = (self.z_bounds[0], self.z_bounds[0] + z_half)
        z_upper = (self.z_bounds[0] + z_half + 1, self.z_bounds[1])

        return [
            SearchBox(
                x_bounds=new_x,
                y_bounds=new_y,
                z_bounds=new_z,
            )
            for new_x, new_y, new_z in triple_iterable(
                (x_lower, x_upper),
                (y_lower, y_upper),
                (z_lower, z_upper),
            )
        ]


@dataclass(frozen=True, eq=True)
class SearchState:
    """
    Represents an intermediate state in the search for the single point which is closest
    to the most Nanobots.

    The state consists of a SearchBox, and the count of Nanobots which intersect with this box.
    """

    search_box: SearchBox
    count_intersecting_bots: int

    def __lt__(self, other: "SearchState"):
        """
        This state will be an entry in a priority queue, and so higher counts of intersecting
        bots should be prioritized. For an equal number of intersecting bots, a smaller box
        should be prioritized.
        """
        if self.count_intersecting_bots > other.count_intersecting_bots:
            return True
        elif self.count_intersecting_bots < other.count_intersecting_bots:
            return False
        else:
            return self.search_box.size > other.search_box.size


def _get_starting_bounding_box(nanobots: List[Nanobot]) -> SearchBox:
    """Builds and returns a SearchBox which fully encloses the provided Nanobots."""

    # Find the min and max x,y,z coordinates across all nanobots.
    minx, maxx = min_and_max(bot.x for bot in nanobots)
    miny, maxy = min_and_max(bot.y for bot in nanobots)
    minz, maxz = min_and_max(bot.z for bot in nanobots)

    # For each axis, determine the largest range the min and max values cover,
    # and find the smallest power of 2 that covers that entire range.
    # It's convenient for all sides to be a power of 2 so that the logic
    # logic of breaking the box into 8 smaller boxes can be kept simple.
    min_size = max([maxx - minx, maxy - miny, maxz - minz])

    # Find the smallest edge length of a cube that is capable of covering the entire
    # field of nanobots, where that edge length is a power of 2.
    box_size = 1
    while box_size < min_size:
        box_size *= 2

    return SearchBox(
        x_bounds=(minx, minx + box_size),
        y_bounds=(miny, miny + box_size),
        z_bounds=(minz, minz + box_size),
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    nanobots = Nanobot.from_lines(stuff)

    # Start with a search field that covers all of the nanobots.
    queue: List[SearchState] = []
    heappush(
        queue,
        SearchState(
            search_box=_get_starting_bounding_box(nanobots),
            count_intersecting_bots=len(nanobots),
        ),
    )

    while queue:
        curr_state = heappop(queue)

        # If the search state is a single point (a box of width 0), then we've
        # found our answer! Return the Manahattan distance from the origin to here.
        if curr_state.search_box.size == 0:
            return manhattan_distance_3d(
                (0, 0, 0),
                (
                    curr_state.search_box.x_bounds[0],
                    curr_state.search_box.y_bounds[0],
                    curr_state.search_box.z_bounds[0],
                ),
            )

        # If we haven't found our answer yet, take the current search box and subdivide
        # it in half along all 3 axes, into 8 smaller boxes.
        for smaller_box in curr_state.search_box.get_smaller_boxes():

            # The count of intersecting nanobots of the box is an upper bound for the
            # number of bots in range of any of the points within that box. By placing
            # each box into a priority queue, the smaller box with the largest number of
            # nearby bots will go to the front of the queue and be checked next.
            #
            # The "best" box (the one with the highest upper bound of nearby bots for a
            # point within the box) will be inspected and again broken in 8 smaller boxes,
            # and the best of those will go to the front of the queue. By the time we have
            # a single point, we know that's the single point with the highest number of
            # nearby bots.
            count_intersecting = smaller_box.get_num_intersecting_bots(nanobots)
            if count_intersecting:
                heappush(
                    queue,
                    SearchState(
                        search_box=smaller_box,
                        count_intersecting_bots=count_intersecting,
                    ),
                )

    raise ValueError("Should have found solution before reaching this point")


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

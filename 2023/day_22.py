from string import ascii_uppercase
from collections import defaultdict
from dataclasses import dataclass
from typing import FrozenSet, Tuple
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 22
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@dataclass
class Brick:
    id: int
    coords: FrozenSet[Tuple[int, int, int]]

    @classmethod
    def from_line(cls, i: int, line: str):
        start, end = line.split("~")
        xs, ys, zs = (int(n) for n in start.split(","))
        xe, ye, ze = (int(n) for n in end.split(","))

        return Brick(
            id=i,
            # id=ascii_uppercase[i],
            coords=frozenset(
                {
                    (x, y, z)
                    for x in range(xs, xe + 1)
                    for y in range(ys, ye + 1)
                    for z in range(zs, ze + 1)
                }
            ),
        )

    @classmethod
    def from_other_brick(cls, other):
        return Brick(
            id=other.id,
            # id=ascii_uppercase[i],
            coords=frozenset(c for c in other.coords),
        )


class BrickCollection:
    def __init__(self, bricks):
        self.brick_locs = defaultdict(lambda: None)
        self.locs_by_brick = defaultdict(list)

        self.bricks = bricks
        self._update_brick_locations()

    def _update_brick_locations(self, brick=None):
        if brick is None:
            self.brick_locs = defaultdict(lambda: None)
            self.locs_by_brick = defaultdict(frozenset)

            for brick in self.bricks:
                for coord in brick.coords:
                    self.brick_locs[coord] = brick
                self.locs_by_brick[brick.id] = frozenset(brick.coords)
        else:
            self.locs_by_brick[brick.id] = frozenset(brick.coords)
            for c in [
                c
                for c, b in self.brick_locs.items()
                if b is not None and b.id == brick.id
            ]:
                del self.brick_locs[c]
            for coord in brick.coords:
                self.brick_locs[coord] = brick

    def settle_all_bricks(self):
        did_any_settle = True
        which_settled = set()
        while did_any_settle:
            did_any_settle = False
            for brick in self.bricks:
                min_z = min([z for x, y, z in brick.coords])
                if all(
                    (z - 1) > 0 and self.brick_locs[(x, y, z - 1)] is None
                    for x, y, z in [(m, n, b) for m, n, b in brick.coords if b == min_z]
                ):
                    # print(f"\nmoving brick {brick.id} down 1")
                    # print(brick.coords)
                    brick.coords = frozenset(
                        [(x, y, z - 1) for x, y, z in brick.coords]
                    )
                    self._update_brick_locations(brick)
                    did_any_settle = True
                    which_settled.add(brick.id)
                    # print(brick.coords)
        return len(which_settled)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    bricks = [Brick.from_line(i, line) for i, line in enumerate(stuff)]
    brick_collection = BrickCollection(bricks)
    brick_collection.settle_all_bricks()
    print("finished settling the first")

    count = 0
    foo = 0

    for j in range(len(stuff)):
        # print(f"testing brick {j}")
        # test_collection = BrickCollection(
        #     [Brick.from_line(i, line) for i, line in enumerate(stuff) if i != j]
        # )
        test_collection = BrickCollection(
            [
                Brick.from_other_brick(other)
                for other in brick_collection.bricks
                if other.id != j
            ]
        )
        asd = test_collection.settle_all_bricks()
        foo += asd

        # if not all(
        #     brick_collection.locs_by_brick[brick_id]
        #     == test_collection.locs_by_brick[brick_id]
        #     for brick_id in [b.id for b in test_collection.bricks]
        # ):
        #     count += 1
        #     foo += asd
        #     # print(f"\nBrick {ascii_uppercase[j]} CAN be disintegrated")
        #     # pprint(brick_collection.locs_by_brick)
        #     # pprint(test_collection.locs_by_brick)
        # else:
        #     foo += asd
        # print(f"\nBrick {ascii_uppercase[j]} cannot be be disintegrated")
        # pprint(brick_collection.locs_by_brick)
        # pprint(test_collection.locs_by_brick)

        # if my_locs_without_b == other_locs:
        #     count += 1
        #     print(f"Brick {ascii_uppercase[j]} can be safely removed")
        #     print(my_locs_without_b)
        #     print(other_locs)
        # else:
        #     print(f"Brick {ascii_uppercase[j]} is supporting others")

    return foo


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    pass


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

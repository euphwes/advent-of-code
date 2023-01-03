from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 3
YEAR = 2018

PART_ONE_DESCRIPTION = "square inches of fabric with overlapping claims"
PART_ONE_ANSWER = 115304

PART_TWO_DESCRIPTION = "ID of claim that does not overlap with any other"
PART_TWO_ANSWER = 275


@dataclass
class FabricClaim:
    id: int
    size_x: int
    size_y: int
    corner_coord: Tuple[int, int]

    @staticmethod
    def from_line(line):
        """Parses a line of the problem input and returns a FabricClaim which gives its ID and
        describes its plot."""

        raw_id, plot_info = line.split(" @ ")
        claim_id = int(raw_id.replace("#", ""))
        raw_coord, raw_size = plot_info.split(": ")
        cx, cy = (int(n) for n in raw_coord.split(","))
        size_x, size_y = (int(n) for n in raw_size.split("x"))

        return FabricClaim(
            id=claim_id,
            size_x=size_x,
            size_y=size_y,
            corner_coord=(cx, cy),
        )

    def covered_fabric(self):
        """Returns a list of the coordinates of all square inches of fabric this Claim
        covers."""

        covered_fabric_coords = list()

        cx, cy = self.corner_coord
        for x in range(cx, cx + self.size_x):
            for y in range(cy, cy + self.size_y):
                covered_fabric_coords.append((x, y))

        return covered_fabric_coords


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(claim_info):

    all_claims = set()
    cell_to_claim_map = defaultdict(set)

    for line in claim_info:

        fabric_claim = FabricClaim.from_line(line)
        all_claims.add(fabric_claim.id)

        for fabric_coord in fabric_claim.covered_fabric():
            cell_to_claim_map[fabric_coord].add(fabric_claim.id)

    return sum(1 for claims_set in cell_to_claim_map.values() if len(claims_set) > 1)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(claim_info):

    all_claims = set()
    cell_to_claim_map = defaultdict(set)

    for line in claim_info:

        fabric_claim = FabricClaim.from_line(line)
        all_claims.add(fabric_claim.id)

        for fabric_coord in fabric_claim.covered_fabric():
            cell_to_claim_map[fabric_coord].add(fabric_claim.id)

    # For every claim ID, check if it's only attached to fabric coordinates where it's the only
    # claim on that coordinate.
    for claim in all_claims:
        has_overlap = False
        for claim_set in cell_to_claim_map.values():
            if claim in claim_set and len(claim_set) > 1:
                has_overlap = True
                break
        if not has_overlap:
            return claim


# ----------------------------------------------------------------------------------------------


def run(input_file):

    claim_info = get_input(input_file)

    part_one(claim_info)
    part_two(claim_info)

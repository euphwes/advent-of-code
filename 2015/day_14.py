from collections.abc import Iterator
from dataclasses import dataclass

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 14
YEAR = 2015

PART_ONE_DESCRIPTION = "Furthest distance traveled by a reindeer"
PART_ONE_ANSWER = 2660

PART_TWO_DESCRIPTION = "Most points obtained by a reindeer"
PART_TWO_ANSWER = 1256


@dataclass
class Reindeer:
    """Dataclass representing a reindeer."""

    name: str
    speed: int
    fly_time: int
    rest_time: int

    def fly(self, total_time: int) -> int:
        """Simulate the reindeer flying for the specified time, and returns distance flown."""

        flight_iterator = self.stepwise_fly()

        for _ in range(total_time - 1):
            next(flight_iterator)
        return next(flight_iterator)

    def stepwise_fly(self) -> Iterator[int]:
        """Simulate the reindeer flying one second at a time.

        Yields the current distance traveled at each time step.
        """

        # Alternate between flying and resting
        distance = 0
        while True:
            for _ in range(self.fly_time):
                distance += self.speed
                yield distance

            for _ in range(self.rest_time):
                yield distance


def _parse_reindeer(raw_input: list[str]) -> list[Reindeer]:
    reindeer = []
    for line in raw_input:
        tokens = line.split()
        reindeer.append(
            Reindeer(
                name=tokens[0],
                speed=int(tokens[3]),
                fly_time=int(tokens[6]),
                rest_time=int(tokens[-2]),
            ),
        )
    return reindeer


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    reindeer = _parse_reindeer(raw_input)

    return max(r.fly(2503) for r in reindeer)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    reindeer = _parse_reindeer(raw_input)

    reindeer_points = {r.name: 0 for r in reindeer}
    reindeer_distances = {r.name: 0 for r in reindeer}
    reindeer_flights = [(r.name, r.stepwise_fly()) for r in reindeer]

    for _ in range(2503):
        for reindeer, flight in reindeer_flights:
            reindeer_distances[reindeer] = next(flight)
        current_winning_distance = max(reindeer_distances.values())
        for reindeer, distance in reindeer_distances.items():
            if distance == current_winning_distance:
                reindeer_points[reindeer] = reindeer_points[reindeer] + 1

    return max(reindeer_points.values())


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

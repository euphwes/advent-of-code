from dataclasses import dataclass
from itertools import combinations
from math import lcm

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 12
YEAR = 2019

PART_ONE_DESCRIPTION = "total energy in the system after 1000 steps"
PART_ONE_ANSWER = 7138

PART_TWO_DESCRIPTION = "how many time steps before history repeats itself"
PART_TWO_ANSWER = 572087463375796


@dataclass
class Moon:
    id: int
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @property
    def potential_energy(self) -> int:  # noqa: D102
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self) -> int:  # noqa: D102
        return abs(self.dx) + abs(self.dy) + abs(self.dz)

    @property
    def total_energy(self) -> int:  # noqa: D102
        return self.potential_energy * self.kinetic_energy


def _parse_moons(raw_input: list[str]) -> list[Moon]:
    moons: list[Moon] = []
    for i, line in enumerate(raw_input):
        clean_line = "".join(x for x in line if x not in "<xyz>= ")
        x, y, z = (int(n) for n in clean_line.split(","))
        moons.append(
            Moon(
                id=i,
                x=x,
                y=y,
                z=z,
                dx=0,
                dy=0,
                dz=0,
            ),
        )
    return moons


def _get_x_cycle_length(moons: list[Moon]) -> int:
    states = {tuple((m.id, m.x, m.dx) for m in moons)}

    while True:
        # Apply velocity delta based on each pair of moons
        for m1, m2 in combinations(moons, r=2):
            if m1.x > m2.x:
                m1.dx -= 1
                m2.dx += 1
            elif m1.x < m2.x:
                m1.dx += 1
                m2.dx -= 1

        # Update position based on velocity
        for moon in moons:
            moon.x += moon.dx

        state = tuple((m.id, m.x, m.dx) for m in moons)
        if state in states:
            return len(states)

        states.add(state)


def _get_y_cycle_length(moons: list[Moon]) -> int:
    states = {tuple((m.id, m.y, m.dy) for m in moons)}

    while True:
        # Apply velocity delta based on each pair of moons
        for m1, m2 in combinations(moons, r=2):
            if m1.y > m2.y:
                m1.dy -= 1
                m2.dy += 1
            elif m1.y < m2.y:
                m1.dy += 1
                m2.dy -= 1

        # Update position based on velocity
        for moon in moons:
            moon.y += moon.dy

        state = tuple((m.id, m.y, m.dy) for m in moons)
        if state in states:
            return len(states)

        states.add(state)


def _get_z_cycle_length(moons: list[Moon]) -> int:
    states = {tuple((m.id, m.z, m.dz) for m in moons)}

    while True:
        # Apply velocity delta based on each pair of moons
        for m1, m2 in combinations(moons, r=2):
            if m1.z > m2.z:
                m1.dz -= 1
                m2.dz += 1
            elif m1.z < m2.z:
                m1.dz += 1
                m2.dz -= 1

        # Update position based on velocity
        for moon in moons:
            moon.z += moon.dz

        state = tuple((m.id, m.z, m.dz) for m in moons)
        if state in states:
            return len(states)

        states.add(state)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    moons = _parse_moons(raw_input)

    for _ in range(1000):
        # First apply velocity delta based on each pair of moons
        for m1, m2 in combinations(moons, r=2):
            # Compare x
            if m1.x > m2.x:
                m1.dx -= 1
                m2.dx += 1
            elif m1.x < m2.x:
                m1.dx += 1
                m2.dx -= 1
            # Compare y
            if m1.y > m2.y:
                m1.dy -= 1
                m2.dy += 1
            elif m1.y < m2.y:
                m1.dy += 1
                m2.dy -= 1
            # Compare z
            if m1.z > m2.z:
                m1.dz -= 1
                m2.dz += 1
            elif m1.z < m2.z:
                m1.dz += 1
                m2.dz -= 1

        # Now update position based on velocity
        for moon in moons:
            moon.x += moon.dx
            moon.y += moon.dy
            moon.z += moon.dz

    return sum(moon.total_energy for moon in moons)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    moons = _parse_moons(raw_input)

    # Since the interaction on each axis (x,y,z) is entirely independent
    # from the other axes, we can just figure out the cycle length for each
    # axis and then find the lowest common multiple of these cycles to find
    # the overall cycle length.
    return lcm(
        _get_x_cycle_length(moons),
        _get_y_cycle_length(moons),
        _get_z_cycle_length(moons),
    )


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

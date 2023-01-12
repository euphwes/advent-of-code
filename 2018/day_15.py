from collections import defaultdict
from dataclasses import dataclass

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 15
YEAR = 2018

PART_ONE_DESCRIPTION = "battle outcome for initial setup"
PART_ONE_ANSWER = 225096

PART_TWO_DESCRIPTION = "battle outcome when elves have min power to win without deaths"
PART_TWO_ANSWER = 35354


# Global "config" flag to differentiate behavior between part 1 and 2.
# In part 2, we'll raise if an elf dies so we can reset and try again with higher elf power.
raise_elf_died = False


AIR = "."
WALL = "#"


class CombatEnded(Exception):
    pass


class ElfDied(Exception):
    pass


def _get_shortest_distance_between(c1, c2, units, cavern):
    """Implement a BFS which finds the distance of the shortest path between two points, inside
    a given cavern (map) layout and info about the current units' positions."""

    queue = []
    queue.append((0, c1))

    visited = set()
    visited.add(c1)

    units_positions = set(u.coord for u in units if u.alive)

    while queue:
        steps, cell = queue.pop(0)
        if cell == c2:
            return steps

        # Find neighboring positions of the current cell which are not cavern walls, and which
        # are not occupied by any living units.
        x, y = cell
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        valid_neighbors = [c for c in neighbors if cavern[c] != WALL]
        valid_neighbors = [c for c in valid_neighbors if c not in units_positions]

        # c2 is usually a target unit we're trying to reach, so it'll show up in `neighbors` but
        # be removed above because it's also another unit's position. Add it back here so we can
        # actually reach it.
        if c2 in neighbors and c2 not in valid_neighbors:
            valid_neighbors.append(c2)

        for n in valid_neighbors:
            if n in visited:
                continue
            visited.add(n)
            queue.append((steps + 1, n))


@dataclass
class Unit:
    unittype: str
    x: int
    y: int
    hp: int
    id: str
    alive: bool
    power: int

    @property
    def coord(self):
        return (self.x, self.y)

    @property
    def neighbors(self):
        return {
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
        }

    def _identify_targets(self, units):
        """Find all living units which are of the opposite type of this unit. Elves attack
        goblins, and vice versa."""

        return [u for u in units if u.unittype != self.unittype and u.alive]

    def _get_walking_targets(self, targets, units, cavern):
        """Get all positions we can walk to which are within range of an enemy unit (immediately
        adjacent, not diagonal, and not a cavern wall or already occupied by a living unit)."""

        walking_targets = set()

        units_positions = set(u.coord for u in units if u.alive)

        for target in targets:
            x, y = target.coord

            adjacents = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            valid_adjacents = [c for c in adjacents if cavern[c] != WALL]
            valid_adjacents = [c for c in valid_adjacents if c not in units_positions]

            for a in valid_adjacents:
                walking_targets.add(a)

        return walking_targets

    def _get_nearest_walking_targets(self, targets, units, cavern):
        """For all positions in the cavern we can walk to which put us immediately in range of
        an enemy unit, return the subset of those which are closest to our current position."""

        walking_targets = self._get_walking_targets(targets, units, cavern)

        distance_to_targets = defaultdict(list)

        for target in walking_targets:
            distance = _get_shortest_distance_between(self.coord, target, units, cavern)
            if distance is None:
                continue
            distance_to_targets[distance].append(target)

        if not distance_to_targets:
            return []

        min_distance = min(distance_to_targets.keys())
        return distance_to_targets[min_distance]

    def _choose_target_by_min_hp(self, targets):
        """Return the enemy target with the lowest HP."""

        targets.sort(key=lambda t: t.hp)
        return targets[0]

    def _attack_target(self, target):
        """Perform an attack on an enemy target."""

        global raise_elf_died

        target.hp -= self.power

        if target.hp <= 0:
            target.alive = False

            # Only raise the ElfDied exception for part 2.
            if target.unittype == "e" and raise_elf_died:
                raise ElfDied()

    def _get_targets_in_range(self, units):
        """Return enemy targets within range to be attacked."""

        targets = self._identify_targets(units)
        if not targets:
            raise CombatEnded()

        # Targets are in range to be attacked if they are immediately adjacent to us.
        return [t for t in targets if t.coord in self.neighbors]

    def _pick_target_and_walk_towards(self, units, cavern):
        """Choose an enemy target and take one step towards it (rules elucidated below)."""

        # These are the positions from which we can attack an enemy unit, that are the closest
        # to our current position.
        nearest_walking_targets = self._get_nearest_walking_targets(
            self._identify_targets(units),
            units,
            cavern,
        )

        if not nearest_walking_targets:
            return

        # Sort the candidate positions to walk towards by "reading order" (x then y coords) and
        # choose the first as the position we want to walk towards.
        nearest_walking_targets.sort(key=lambda c: c[0])
        nearest_walking_targets.sort(key=lambda c: c[1])
        walk_target = nearest_walking_targets[0]

        # Find positions neighboring us right now, which we can step into (not a cavern wall or
        # otherwise occupied by a living unit.)
        units_positions = set(u.coord for u in units if u.alive)
        valid_neighbors = [c for c in self.neighbors if cavern[c] != WALL]
        valid_neighbors = [c for c in valid_neighbors if c not in units_positions]

        # For each position adjacent to our current position, find the distance between that and
        # the final enemy-adjacent position we want to reach.
        distances_to_neighbors = defaultdict(list)
        for n in valid_neighbors:
            d = _get_shortest_distance_between(n, walk_target, units, cavern)
            if d is None:
                continue
            distances_to_neighbors[d].append(n)

        # Find which places we can step (1 step away) which are closest to the target
        # enemy-adjacent position we want to walk towards.
        min_d = min(distances_to_neighbors.keys())
        candidates = distances_to_neighbors[min_d]

        # Sort those 1 step away positions by reading order (x then y coords), and choose the
        # first as the step we're going to take this turn.
        candidates.sort(key=lambda c: c[0])
        candidates.sort(key=lambda c: c[1])
        nx, ny = candidates[0]

        # Move this unit to that position.
        self.x = nx
        self.y = ny

    def perform_turn(self, units, cavern):
        """Executes one turn for this unit."""

        # Dead people can't do anything.
        if not self.alive:
            return

        # If there aren't any targets within range right now, pick the best to walk towards
        # and walk towards it.
        if not self._get_targets_in_range(units):
            self._pick_target_and_walk_towards(units, cavern)

        # Find targets within range of attack now.
        targets_in_range = self._get_targets_in_range(units)

        # If none, our turn is done because we've already walked.
        if not targets_in_range:
            return

        # Otherwise choose a target and attack.
        chosen_target = self._choose_target_by_min_hp(targets_in_range)
        self._attack_target(chosen_target)


def _parse_units(grid, elf_power=3):
    """Parse unit information out of the problem input."""

    curr_unit_id = 0
    units = list()

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell not in "EG":
                continue

            if cell == "E":
                unittype = "e"
                unit_id = f"E-{curr_unit_id}"
                power = elf_power
            else:
                unittype = "g"
                unit_id = f"G-{curr_unit_id}"
                power = 3

            curr_unit_id += 1

            units.append(
                Unit(
                    id=unit_id,
                    unittype=unittype,
                    x=x,
                    y=y,
                    hp=200,
                    alive=True,
                    power=power,
                )
            )

    return units


def _parse_cavern(grid):
    """Parse a map of the cavern walls and open space from the problem input."""

    cavern = defaultdict(lambda: WALL)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):

            # Positions occupied by a unit we're going to call "air" for the purpose of this
            # dict, because we CAN go there if we determine it's not already occupied by a unit.
            # That'll be a problem for elsewhere in the solution.
            cavern[(x, y)] = WALL if cell == WALL else AIR

    return cavern


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(populated_cavern):
    cavern = _parse_cavern(populated_cavern)
    units = _parse_units(populated_cavern)

    for round in int_stream():

        try:
            units.sort(key=lambda u: u.x)
            units.sort(key=lambda u: u.y)

            for unit in units:
                unit.perform_turn(units, cavern)

        except CombatEnded:
            remaining = [u.hp for u in units if u.alive]
            return sum(remaining) * round


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(populated_cavern):

    global raise_elf_died
    raise_elf_died = True

    elf_power = 5
    counting_up = True

    last_successful_outcome = None

    while True:
        cavern = _parse_cavern(populated_cavern)
        units = _parse_units(populated_cavern, elf_power=elf_power)

        for round in int_stream():

            try:
                units.sort(key=lambda u: u.x)
                units.sort(key=lambda u: u.y)

                for unit in units:
                    unit.perform_turn(units, cavern)

            except CombatEnded:
                remaining = [u.hp for u in units if u.alive]

                last_successful_outcome = sum(remaining) * round
                counting_up = False
                elf_power -= 1
                break

            except ElfDied:
                if counting_up:
                    elf_power += 5
                    break
                else:
                    return last_successful_outcome


# ----------------------------------------------------------------------------------------------


def run(input_file):

    populated_cavern = get_input(input_file)

    part_one(populated_cavern)
    part_two(populated_cavern)

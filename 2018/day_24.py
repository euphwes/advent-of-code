from dataclasses import dataclass
from typing import List, Optional, Tuple
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 24
YEAR = 2018

PART_ONE_DESCRIPTION = "units left for the winning army in the initial battle"
PART_ONE_ANSWER = 14799

PART_TWO_DESCRIPTION = "immune system units left after minimum boost needed to win"
PART_TWO_ANSWER = 4428


@dataclass
class Group:

    army_id: str
    id: str

    remaining_units: int

    # Properties for each unit
    hp: int
    immunities: List[str]
    weaknesses: List[str]
    atk: int
    attack_type: str
    initiative: int

    @property
    def effective_power(self) -> int:
        return self.remaining_units * self.atk

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Army:
    id: str
    groups: List[Group]

    @property
    def remaining_units(self) -> int:
        return sum(group.remaining_units for group in self.groups)


def _parse_units(line):
    """
    1994 units each with 484 hit points with an attack that does 46 cold damage at initiative 3
    --> 1994
    """
    return int(line.split(" ")[0])


def _parse_initiative(line):
    """
    1994 units each with 484 hit points with an attack that does 46 cold damage at initiative 3
    --> 3
    """
    return int(line.split(" ")[-1])


def _parse_hp(line):
    """
    1994 units each with 484 hit points with an attack that does 46 cold damage at initiative 3
    --> 484
    """
    start_ix = line.index("each with") + 10
    end_ix = line.index("hit")
    return int(line[start_ix:end_ix].strip())


def _parse_atk(line):
    """
    1994 units each with 484 hit points with an attack that does 46 cold damage at initiative 3
    --> 46
    """
    start_ix = line.index("that does") + 10
    end_ix = line.index("damage")
    return int(line[start_ix:end_ix].strip().split(" ")[0])


def _parse_atk_type(line):
    """
    1994 units each with 484 hit points with an attack that does 46 cold damage at initiative 3
    --> 'cold'
    """
    start_ix = line.index("that does") + 10
    end_ix = line.index("damage")
    return line[start_ix:end_ix].strip().split(" ")[1]


def _parse_weaknesses(line):
    """
    42 units each with 41601 hit points (weak to radiation; immune to fire) ...
    --> ['radiation']

    1561 units each with 10633 hit points (weak to radiation, cold) ...
    --> ['radiation', 'cold']
    """
    if "(" not in line:
        return []

    substr = line[line.index("(") + 1 : line.index(")")]

    if ";" in substr:
        for split in substr.split("; "):
            if "weak to" in split:
                return split.replace("weak to", "").strip().split(", ")

    elif "weak to" in substr:
        return substr.replace("weak to", "").strip().split(", ")

    return []


def _parse_immunities(line):
    """
    42 units each with 41601 hit points (immune to slashing) ...
    --> ['slashing']

    1561 units each with 15 hit points (weak to radiation; immune to bludgeoning, cold) ...
    --> ['bludgeoning', 'cold']
    """
    if "(" not in line:
        return []

    substr = line[line.index("(") + 1 : line.index(")")]

    if ";" in substr:
        for split in substr.split("; "):
            if "immune to" in split:
                return split.replace("immune to", "").strip().split(", ")

    elif "immune to" in substr:
        return substr.replace("immune to", "").strip().split(", ")

    return []


def _parse_armies(army_info) -> Tuple[Army, Army]:
    immune = Army(id="immune", groups=[])
    infection = Army(id="infection", groups=[])
    curr_army = immune

    for line in army_info[1:]:
        if not line:
            continue
        if "Infection:" in line:
            curr_army = infection
            continue

        curr_army.groups.append(
            Group(
                id=f"{curr_army.id}{len(curr_army.groups)+1}",
                army_id=curr_army.id,
                hp=_parse_hp(line),
                atk=_parse_atk(line),
                attack_type=_parse_atk_type(line),
                remaining_units=_parse_units(line),
                initiative=_parse_initiative(line),
                weaknesses=_parse_weaknesses(line),
                immunities=_parse_immunities(line),
            )
        )

    return immune, infection


def _calc_total_dmg(attacker, defender):
    if attacker.attack_type in defender.immunities:
        return 0
    if attacker.attack_type in defender.weaknesses:
        return attacker.effective_power * 2
    return attacker.effective_power


def _simulate_battle(immune: Army, infection: Army) -> Optional[Army]:

    # Each loop is one "turn" of battle
    while True:
        # -----------------------
        # Target selection phase
        # -----------------------

        # Gather all groups across both armies that still have units left.
        participating_groups = [
            group for group in immune.groups + infection.groups if group.remaining_units
        ]

        # Targets are chosen in order of highest effective power, with ties broken by initiative
        participating_groups.sort(key=lambda t: t.initiative, reverse=True)
        participating_groups.sort(key=lambda t: t.effective_power, reverse=True)

        # Maintain a mapping of each attacking group and the target they choose to attack
        groups_and_targets = dict()

        for attacking_group in participating_groups:
            # Calculate the potential damage done to each defending group
            defending_options = [
                (g, _calc_total_dmg(attacking_group, g))
                for g in participating_groups
                if (
                    g not in groups_and_targets.values()
                    and g.army_id != attacking_group.army_id
                )
            ]

            # For each defending group, we prioritize first by most damage. Break any ties
            # by highest effective power of the defending group, then by highest initiative.
            defending_options.sort(key=lambda t: t[0].initiative, reverse=True)
            defending_options.sort(key=lambda t: t[0].effective_power, reverse=True)
            defending_options.sort(key=lambda t: t[1], reverse=True)

            # If there is nobody for the attacking group to attack, record that.
            if not defending_options:
                groups_and_targets[attacking_group] = None

            # Otherwise choose the "best" option of defending group
            else:
                defending_group, potential_damage = defending_options[0]
                if potential_damage == 0:
                    groups_and_targets[attacking_group] = None
                else:
                    groups_and_targets[attacking_group] = defending_group

        # -----------------------
        # Attacking phase
        # -----------------------

        total_units_killed_this_round = 0

        # Order all participating groups by their initiative;
        # this the order in which# they will attack.
        attacking_order = [g for g in participating_groups]
        attacking_order.sort(key=lambda g: g.initiative, reverse=True)

        # In order, simulate one group attacking their chosen target.
        for attacking_group in attacking_order:
            # This group might have been killed by their attacker already,
            # prior to their turn to attack. If the group is dead, skip it.
            if attacking_group.remaining_units == 0:
                continue

            # If the attacking group didn't have a target, skip their turn
            defending_group = groups_and_targets[attacking_group]
            if defending_group is None:
                continue

            # Recalculate the damage the attacking group can deal to the defending group,
            # based on their current remaining units and the defense's immunities/weaknesses.
            total_dmg = _calc_total_dmg(attacking_group, defending_group)

            # Figure out how many defending units can be killed. Only whole numbers of units
            # can be taken out; any fractional damage is ignored. You can only kill up to the
            # number of units remaining.
            units_killed = min(
                (total_dmg // defending_group.hp), defending_group.remaining_units
            )

            # Substract the killed units from the defending group and tally the deaths in the
            # round's total kill count.
            defending_group.remaining_units -= units_killed
            total_units_killed_this_round += units_killed

        # It's possible the battle can be "stalled"; that is, all attacking groups aren't able
        # to deal any damage to their defending group due to the selection strategy and current
        # stats. If this happens, the battle will be stalled because no more units will ever
        # be killed. Just return `None` indicating "no winning army".
        if total_units_killed_this_round == 0:
            return None

        # Check if any of the armies have won; if their opponent army's total remaining units
        # are zero.
        if immune.remaining_units == 0:
            return infection

        if infection.remaining_units == 0:
            return immune


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    immune, infection = _parse_armies(stuff)

    winner = _simulate_battle(immune, infection)

    assert winner
    return winner.remaining_units


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    curr_boost = 0
    while True:
        immune, infection = _parse_armies(stuff)

        curr_boost += 1
        for group in immune.groups:
            group.atk += curr_boost

        winner = _simulate_battle(immune, infection)
        if winner and winner.id == "immune":
            return winner.remaining_units


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

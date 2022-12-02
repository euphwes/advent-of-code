from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

from itertools import combinations

#---------------------------------------------------------------------------------------------------

ALIVE = 'status_alive'
DEAD  = 'status_dead'

class Item:
    def __init__(self, name, cost, damage, armor):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __repr__(self):
        return self.name


class Actor:
    def __init__(self, hp, items):
        self.hp = hp
        self.items = items
        self.damage = sum(item.damage for item in self.items)
        self.armor = sum(item.armor for item in self.items)
        self.item_cost = sum(item.cost for item in self.items)
        self.status = ALIVE

    def take_damage(self, raw_damage):
        """ Takes damage frow the raw damage supplied, offset by armor. """

        self.hp -= max(raw_damage - self.armor, 1)
        if self.hp <= 0:
            self.status = DEAD


def simulate_battle(player, boss):
    """ Simulates a battle between the supplied player Actor and boss Actor. Returns the victor. """

    while True:
        # player attacks boss
        boss.take_damage(player.damage)
        if boss.status == DEAD:
            return player

        # boss attacks player
        player.take_damage(boss.damage)
        if player.status == DEAD:
            return boss

#---------------------------------------------------------------------------------------------------

weapons = [
    Item('Dagger',      8, 4, 0),
    Item('Shortsword', 10, 5, 0),
    Item('Warhammer',  25, 6, 0),
    Item('Longsword',  40, 7, 0),
    Item('Greataxe',   74, 8, 0)
]

armors = [
    Item('None',        0, 0, 0),
    Item('Leather',    13, 0, 1),
    Item('Chainmail',  31, 0, 2),
    Item('Splintmail', 53, 0, 3),
    Item('Bandemail',  75, 0, 4),
    Item('Platemail', 102, 0, 5)
]

rings = [
    Item('Damage +1',  25, 1, 0),
    Item('Damage +2',  50, 2, 0),
    Item('Damage +3', 100, 3, 0),
    Item('Defense +1', 20, 0, 1),
    Item('Defense +2', 40, 0, 2),
    Item('Defense +3', 80, 0, 3)
]


def get_item_combos():
    """ Yields all valid combinations of items, each set as a list. """

    for weapon, armor in nested_iterable(weapons, armors):
        for num_rings in range(3):
            for ring_combo in combinations(rings, num_rings):
                items = [weapon, armor]
                items.extend(ring_combo)
                yield items

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 21, 1, 'minimum gold to spend and still win', assert_answer=78)
def part_one():
    costs_of_winning_item_combos = list()
    for items in get_item_combos():
        player = Actor(100, items)

        boss = Actor(104, list())
        boss.damage = 8
        boss.armor = 1

        winner = simulate_battle(player, boss)
        if winner is player:
            costs_of_winning_item_combos.append(player.item_cost)

    return min(costs_of_winning_item_combos)


@aoc_output_formatter(2015, 21, 2, 'maximum gold to spend and still lose', assert_answer=148)
def part_two():
    costs_of_losing_item_combos = list()
    for items in get_item_combos():
        player = Actor(100, items)

        boss = Actor(104, list())
        boss.damage = 8
        boss.armor = 1

        winner = simulate_battle(player, boss)
        if winner is boss:
            costs_of_losing_item_combos.append(player.item_cost)

    return max(costs_of_losing_item_combos)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one()
    part_two()

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

from itertools import combinations
from random import choice

#---------------------------------------------------------------------------------------------------

_IS_HARD = False

_ACTIVE_EFFECTS = list()
_ACTIVE_EFFECT_NAMES = list()

#---------------------------------------------------------------------------------------------------

class ActorState:
    ALIVE = 'status_alive'
    DEAD  = 'status_dead'


class Actor:
    def __init__(self, hp, mana):
        self.hp = hp
        self.mana = mana
        self.armor = 0
        self.status = ActorState.ALIVE
        self.spent_mana = 0

    def take_damage(self, raw_damage):
        self.hp -= max(raw_damage - self.armor, 1)
        if self.hp <= 0:
            self.status = ActorState.DEAD

    def heal(self, amount):
        self.hp += amount


def magic_missile_spell(player, boss):
    boss.take_damage(4)


def drain_spell(player, boss):
    boss.take_damage(2)
    player.heal(2)


def shield_spell(player, boss):
    _ACTIVE_EFFECT_NAMES.append('shield_spell')
    player.armor += 7

    def lower_defense():
        player.armor -= 7
        _ACTIVE_EFFECT_NAMES.remove('shield_spell')

    def gen():
        for _ in range(6):
            yield lambda: None
        yield lower_defense

    return gen()


def poison_spell(player, boss):
    _ACTIVE_EFFECT_NAMES.append('poison_spell')

    def apply_poison():
        boss.take_damage(3)

    def apply_final():
        boss.take_damage(3)
        _ACTIVE_EFFECT_NAMES.remove('poison_spell')

    def gen():
        for _ in range(5):
            yield apply_poison
        yield apply_final

    return gen()


def recharge_spell(player, boss):
    _ACTIVE_EFFECT_NAMES.append('recharge_spell')

    def apply_recharge():
        player.mana += 101

    def apply_final():
        player.mana += 101
        _ACTIVE_EFFECT_NAMES.remove('recharge_spell')

    def gen():
        for _ in range(4):
            yield apply_recharge
        yield apply_final

    return gen()


spell_cost_map = {
    magic_missile_spell: 53,
    drain_spell: 73,
    shield_spell: 113,
    poison_spell: 173,
    recharge_spell: 229
}

#---------------------------------------------------------------------------------------------------

def simulate_battle(player, boss):
    """ Simulates a battle between the supplied player Actor and boss Actor. Returns the victor. """

    def apply_active_effects():
        for effect_itr in _ACTIVE_EFFECTS:
            if effect_itr:
                try:
                    next(effect_itr)()
                except StopIteration:
                    pass

    def get_available_spells(player):
        available_spells = [[s, m] for s, m in spell_cost_map.items() if m <= player.mana and s.__name__ not in _ACTIVE_EFFECT_NAMES]
        # print('')
        # print('player mana: ' + str(player.mana))
        # print('available: ' + str([a.__name__ for a, m in available_spells]))
        # print('active: ' + str(_ACTIVE_EFFECT_NAMES))
        return available_spells

    while True:
        if _IS_HARD:
            player.hp -= 1
            if player.hp <= 0:
                return boss

        apply_active_effects()
        if boss.status == ActorState.DEAD:
            return player

        chosen_spell, mana_cost = choice(get_available_spells(player))
        # print('casting {} for {} mana'.format(chosen_spell.__name__, mana_cost))
        player.mana -= mana_cost
        player.spent_mana += mana_cost
        _ACTIVE_EFFECTS.append(chosen_spell(player, boss))
        if boss.status == ActorState.DEAD:
            return player

        apply_active_effects()
        player.take_damage(boss.damage)
        if boss.status == ActorState.DEAD:
            return player
        if player.status == ActorState.DEAD:
            return boss

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 22, 1, 'minimum mana to spend and still win', assert_answer=900)
def part_one():
    global _ACTIVE_EFFECTS, _ACTIVE_EFFECT_NAMES

    winning_mana_costs = list()

    for _ in range(20000):
    	_ACTIVE_EFFECT_NAMES = list()
    	_ACTIVE_EFFECTS = list()

    	player = Actor(50, 500)

    	boss = Actor(51, 0)
    	boss.damage = 9

    	try:
    		winner = simulate_battle(player, boss)
    		if winner is player:
    			winning_mana_costs.append(player.spent_mana)
    	except IndexError:
    		pass

    return min(winning_mana_costs)


@aoc_output_formatter(2015, 22, 2, 'minimum mana to spend and still win on hard', assert_answer=1216)
def part_two():
    global _IS_HARD, _ACTIVE_EFFECTS, _ACTIVE_EFFECT_NAMES
    _IS_HARD = True

    winning_mana_costs = list()

    for _ in range(20000):
    	_ACTIVE_EFFECT_NAMES = list()
    	_ACTIVE_EFFECTS = list()

    	player = Actor(50, 500)

    	boss = Actor(51, 0)
    	boss.damage = 9

    	try:
    		winner = simulate_battle(player, boss)
    		if winner is player:
    			winning_mana_costs.append(player.spent_mana)
    	except IndexError:
    		pass

    return min(winning_mana_costs)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one()
    part_two()

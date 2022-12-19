from collections import defaultdict
from enum import Enum

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 19
YEAR = 2022

PART_ONE_DESCRIPTION = "sum of quality level of all blueprints"
PART_ONE_ANSWER = 1480

PART_TWO_DESCRIPTION = "product of geodes found in 32 min with first 3 blueprints"
PART_TWO_ANSWER = 3168


class RobotType(Enum):
    ORE = "ore"
    CLAY = "clay"
    GEODE = "geode"
    OBSIDIAN = "obsidian"


class ResourceType(Enum):
    ORE = "ore"
    CLAY = "clay"
    GEODE = "geode"
    OBSIDIAN = "obsidian"


def _parse_blueprint(blueprint):
    """Parse a line of the input, returning a dictionary which maps robot types to their cost
    in each type of resource to manufacture a new one."""

    robot_resource_costs = {
        RobotType.ORE: defaultdict(int),
        RobotType.CLAY: defaultdict(int),
        RobotType.GEODE: defaultdict(int),
        RobotType.OBSIDIAN: defaultdict(int),
    }

    # Trim off the "Blueprint ##: " portion of the line
    after_colon_ix = blueprint.index(":") + 2
    blueprint = blueprint[after_colon_ix:]

    # Chunk the remainder into "each ____ robot costs ____". There will be 4 of these,
    # corresponding to the following robot types: (ore, clay, obsidian, geode) in that order.
    pieces = blueprint.split(". ")
    for i, piece in enumerate(pieces):

        # Within a line that looks like:
        # Each obsidian robot costs 4 ore and 11 clay
        # Just try to convert each word to an integer. If it succeeds, it's the cost in some
        # type of resource to make that robot. Keep track of the numbers we find, we can figure
        # out how to interpret those later.
        resource_costs = list()
        for word in piece.split():
            try:
                resource_costs.append(int(word))
            except:
                pass

        # Every robot requires ore to make, and it's always specified first.
        ore_cost = resource_costs.pop(0)

        if i == 0:
            # Ore robot is first, and only requires ore to make.
            robot_resource_costs[RobotType.ORE][ResourceType.ORE] = ore_cost

        elif i == 1:
            # Clay robot is second, and only requires ore to make.
            robot_resource_costs[RobotType.CLAY][ResourceType.ORE] = ore_cost

        elif i == 2:
            # Obsidian robot is third, it also requires clay.
            clay_cost = resource_costs.pop(0)
            robot_resource_costs[RobotType.OBSIDIAN][ResourceType.ORE] = ore_cost
            robot_resource_costs[RobotType.OBSIDIAN][ResourceType.CLAY] = clay_cost

        else:
            # Geode robot is last, it also requires obsidian.
            obsidian_cost = resource_costs.pop(0)
            robot_resource_costs[RobotType.GEODE][ResourceType.ORE] = ore_cost
            robot_resource_costs[RobotType.GEODE][ResourceType.OBSIDIAN] = obsidian_cost

    return robot_resource_costs


def _calculate_bot_limits(blueprint):
    """Calculate the maximum number of ore, clay, and obsidian bots we should manufacture based
    on a given blueprint, so that we don't end up producing more of a given resource than we can
    actually use."""

    max_ore_bots = 0
    max_clay_bots = 0
    max_obs_bots = 0
    for cost in blueprint.values():
        max_ore_bots = max([max_ore_bots, cost[ResourceType.ORE]])
        max_clay_bots = max([max_clay_bots, cost[ResourceType.CLAY]])
        max_obs_bots = max([max_obs_bots, cost[ResourceType.OBSIDIAN]])

    return max_ore_bots, max_clay_bots, max_obs_bots


def _get_possible_geodes_found(
    time_left,
    blueprint,
    bots_owned,
    resources_owned,
    bot_limits,
    should_perform_previous_afford_check=False,
    previous_resources=None,
):

    # Decompose bots_owned, resources_owned, and previous_resources_owned into individual
    # variables for easier readier later.
    ore_bots, clay_bots, obsidian_bots, geode_bots = bots_owned
    ore, clay, obsidian, geode = resources_owned

    previous_ore, previous_clay, previous_obsidian = (
        (0, 0, 0) if previous_resources is None else previous_resources
    )

    max_ore_bots, max_clay_bots, max_obs_bots = bot_limits

    # If there's no time remaining, then however many geodes we have is what we have.
    if time_left == 0:
        return [geode]

    # Prefer bots in this order. Intuitively we should always make a geode bot if we are able
    # because geodes are the resource we want to maximize. Similarly, we should always make an
    # obsidian bot if able because they yield obsidian which is the limiting resource to make
    # geode robots which produce our target resource.
    bot_precedence_order = [
        RobotType.GEODE,
        RobotType.OBSIDIAN,
        RobotType.CLAY,
        RobotType.ORE,
    ]

    # Remember if we built a geode bot or obsidian bot.
    did_build_geode_bot = False
    did_build_obsidian_bot = False

    # Track the possibilities for how many geodes we could end up with based on the choices we
    # make below.
    possible_geode_outcomes = []

    for bot_type in bot_precedence_order:
        costs = blueprint[bot_type]

        # First check if we can afford this type of bot. If we can't, there's nothing to
        # consider, we just move on and check the next type.
        if ore < costs[ResourceType.ORE]:
            continue
        if clay < costs[ResourceType.CLAY]:
            continue
        if obsidian < costs[ResourceType.OBSIDIAN]:
            continue

        # Next check if we've reached the maximum limit for this type of bot. If we have, just
        # continue on to check the next type of bot. There's no use in increasing ore, clay, or
        # obsidian bot count if that means we'll be producing a resource faster than we use it.
        if bot_type == RobotType.ORE and ore_bots >= max_ore_bots:
            continue
        if bot_type == RobotType.CLAY and clay_bots >= max_clay_bots:
            continue
        if bot_type == RobotType.OBSIDIAN and obsidian_bots >= max_obs_bots:
            continue

        # If I *could* have afforded this specific type of bot last minute but didn't choose to
        # build it, then I shouldn't build it now, because it would have been better to build it
        # last round (to yield 1 more total resource). I should only consider building a
        # different bot this time.
        #
        # Example: I could have afforded to build an ore bot last time, but I chose not to.
        # Now I can build a clay bot this round, which requires more ore.
        if should_perform_previous_afford_check:

            could_afford_last_minute = True
            if previous_ore < costs[ResourceType.ORE]:
                could_afford_last_minute = False
            if previous_clay < costs[ResourceType.CLAY]:
                could_afford_last_minute = False
            if previous_obsidian < costs[ResourceType.OBSIDIAN]:
                could_afford_last_minute = False

            if could_afford_last_minute:
                continue

        # We made it here, finally! There's no reason not to build whatever robot type we're on.
        # Add 1 to the type of robot we're making this round, so we can pass it on.
        next_bots_owned = (
            ore_bots + (1 if bot_type == RobotType.ORE else 0),
            clay_bots + (1 if bot_type == RobotType.CLAY else 0),
            obsidian_bots + (1 if bot_type == RobotType.OBSIDIAN else 0),
            geode_bots + (1 if bot_type == RobotType.GEODE else 0),
        )

        # Let's calculate resources after this round --
        # 1 new resource of each type for each robot mining that type, less the amount of
        # resources it costs to make the robot we selected.
        next_resources_owned = (
            ore + ore_bots - costs[ResourceType.ORE],
            clay + clay_bots - costs[ResourceType.CLAY],
            obsidian + obsidian_bots - costs[ResourceType.OBSIDIAN],
            geode + geode_bots,
        )

        # Recursively check how many geodes we might possibility end up with, after we update
        # our robot count and resources based on the robot we just made.
        possible_geode_outcomes.extend(
            _get_possible_geodes_found(
                time_left - 1,
                blueprint,
                next_bots_owned,
                next_resources_owned,
                bot_limits,
                should_perform_previous_afford_check=False,
                previous_resources=None,
            )
        )

        # If we built a geode or obsidian robot, that's always the best move. Remember that and
        # break early so we don't check other robot types with lower precedence. Remember if we
        # built one of these types of robots.
        if bot_type == RobotType.GEODE:
            did_build_geode_bot = True
            break
        if bot_type == RobotType.OBSIDIAN:
            did_build_obsidian_bot = True
            break

    # If we built a geode or an obsidian robot this round, that's always the best choice and we
    # don't need to check the outcomes if we didn't build that robot. However, if we built an
    # ore or a clay robot, we should still check the no-new-robots options because it might be
    # better in the long run to save up the ore that we built on those.
    #
    # Set should_perform_previous_afford_check=True, because next round we should avoid building
    # the same robot that we chose not to build this time.
    if not (did_build_geode_bot or did_build_obsidian_bot):
        possible_geode_outcomes.extend(
            _get_possible_geodes_found(
                time_left - 1,
                blueprint,
                (ore_bots, clay_bots, obsidian_bots, geode_bots),
                (
                    ore + ore_bots,
                    clay + clay_bots,
                    obsidian + obsidian_bots,
                    geode + geode_bots,
                ),
                bot_limits,
                should_perform_previous_afford_check=True,
                previous_resources=(ore, clay, obsidian),
            )
        )

    return possible_geode_outcomes


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one_v2(raw_blueprints):

    blueprints = {
        i + 1: _parse_blueprint(line) for i, line in enumerate(raw_blueprints)
    }

    score = 0
    for blueprint_id, blueprint in blueprints.items():

        possible_geodes = _get_possible_geodes_found(
            24,
            blueprint,
            (1, 0, 0, 0),
            (0, 0, 0, 0),
            _calculate_bot_limits(blueprint),
        )

        score += blueprint_id * max(possible_geodes)

    return score


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_blueprints):

    blueprints = [_parse_blueprint(line) for line in raw_blueprints[:3]]

    score = 1
    for blueprint in blueprints:

        possible_geodes = _get_possible_geodes_found(
            32,
            blueprint,
            (1, 0, 0, 0),
            (0, 0, 0, 0),
            _calculate_bot_limits(blueprint),
        )

        score *= max(possible_geodes)

    return score


# ----------------------------------------------------------------------------------------------


def run(input_file):

    raw_blueprints = get_input(input_file)
    part_one_v2(raw_blueprints)

    raw_blueprints = get_input(input_file)
    part_two(raw_blueprints)

from collections import Counter
from math import ceil

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 14
YEAR = 2019

PART_ONE_DESCRIPTION = "total amount of ORE required to produce 1 FUEL"
PART_ONE_ANSWER = 783895

PART_TWO_DESCRIPTION = "max amount of FUEL produceable with 1 trillion ORE"
PART_TWO_ANSWER = 1896688

# A quantity of a material produced or required
# e.g. (10, "A") for 10 units of "A"
# e.g. (24, "FUEL") for 24 units of "FUEL"
MaterialQuantity = tuple[int, str]


def _parse_material_map(
    raw_input: list[str],
) -> dict[MaterialQuantity, set[MaterialQuantity]]:
    """Parse a dictionary of output material to the input material(s)."""

    material_map: dict[MaterialQuantity, set[MaterialQuantity]] = {}

    for line in raw_input:
        # Example:
        # "2 AB, 3 BC, 4 CA => 1 FUEL"

        # input_side = "2 AB, 3 BC, 4 CA"
        # output_side = "1 FUEL"
        input_side, output_side = line.split(" => ")

        # Get the MaterialQuantity tuple for the output side
        output_pieces = output_side.split(" ")
        output_quantity = (int(output_pieces[0]), output_pieces[1])

        # Get the set of MaterialQuantity tuples for the input side
        input_quantities = set()
        for input_element in input_side.split(", "):
            input_pieces = input_element.split(" ")
            input_quantities.add((int(input_pieces[0]), input_pieces[1]))

        material_map[output_quantity] = input_quantities

    return material_map


def _find_material_requirements(
    target_material: str,
    material_map: dict[MaterialQuantity, set[MaterialQuantity]],
) -> tuple[MaterialQuantity, set[MaterialQuantity]]:
    """For a given target material, return the required material to make it.

    Returns a tuple of (MaterialQuantity) for the output material produced, and
    the set of input MaterialQuantity required to produce that output.
    """
    for material_qty, requirements in material_map.items():
        _, material_name = material_qty
        if material_name == target_material:
            return (material_qty, requirements)

    msg = f"Material {target_material} not found in material_map"
    raise ValueError(msg)


def _get_full_set_of_materials_a_material_decomposes_through(
    target_material: str,
    material_map: dict[MaterialQuantity, set[MaterialQuantity]],
) -> set[str]:
    """For a given target material, return all transitive components.

    Ex:
    1 AB + 2 BC => 1 ABC
    3 BC + 1 CD => 1 BCD
    1 ABC + 1 BCD => 1 ABCD

    ABCD needs {AB, BC, CD, ABC, BCD} to be produced.
    """
    if target_material == "ORE":
        return set()

    _, mats = _find_material_requirements(target_material, material_map)

    constituent_mats = {mat for _, mat in mats}

    reqs = constituent_mats
    others = set()
    for submat in constituent_mats:
        others.update(
            _get_full_set_of_materials_a_material_decomposes_through(submat, material_map),
        )

    reqs.update(others)
    return reqs


def _find_next_material_to_decompose(
    requirements: set[MaterialQuantity],
    material_map: dict[MaterialQuantity, set[MaterialQuantity]],
) -> MaterialQuantity:
    # Don't want to decompose any material X yet if another material in the
    # requirements also decomposes to X. We want to fully consolidate the total
    # amount of X we need before we decompose X.

    for qty, mat in requirements:
        if mat == "ORE":
            continue
        if any(
            mat
            in _get_full_set_of_materials_a_material_decomposes_through(other_mat, material_map)
            for _, other_mat in requirements
            if other_mat != "ORE"
        ):
            continue
        return (qty, mat)

    raise ValueError


def _consolidate_material_requirements(
    requirements: set[MaterialQuantity],
) -> set[MaterialQuantity]:
    counter = Counter()
    for qty, material in requirements:
        counter[material] += qty

    return {(counter[mat], mat) for mat in counter}


def _calc_ore_required_for_fuel_amount(
    fuel_target: int,
    material_map: dict[MaterialQuantity, set[MaterialQuantity]],
) -> int:
    # We'll use this set of materials to hold the required ORE
    # to produce 1 FUEL. At each step, anything in here that's not "ORE"
    # we'll decompose into the contituents required to produce that material
    # until all we're left with is ORE.
    total_required_materials: set[MaterialQuantity] = {(fuel_target, "FUEL")}

    while not all(mat == "ORE" for _, mat in total_required_materials):
        # Find any item in the required materials that's not raw ORE.
        # Remove that from the list.
        target_material_quantity = _find_next_material_to_decompose(
            total_required_materials,
            material_map,
        )
        total_required_materials.remove(target_material_quantity)

        # Figure out what the required constituents are for this material
        target_quantity, target_material = target_material_quantity
        output_qty, requirements = _find_material_requirements(target_material, material_map)

        # Some reactions produce N qty of a material, but we need X qty (where X > N).
        # We might need to run a reaction ceil(X / N) times to get the right amount.
        # Ex: need 3 ABC
        # 1 A, 2 B, 1 C => 2 ABC
        # So we need ceil(3/2) == 2x the reactions to get enough ABC
        factor = ceil(target_quantity / output_qty[0])
        for qty_required, mat_required in requirements:
            total_required_materials.add((factor * qty_required, mat_required))

        total_required_materials = _consolidate_material_requirements(total_required_materials)

    return sum(qty for qty, _ in total_required_materials)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return _calc_ore_required_for_fuel_amount(
        fuel_target=1,
        material_map=_parse_material_map(raw_input=raw_input),
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    material_map = _parse_material_map(raw_input=raw_input)

    max_fuel_so_far = -1

    # Started at 1_275_681 as a naive (1 trillion / ore per fuel from part 1) guess.
    # Printed debug and then manually jumped up until I saw the ORE
    # requirements were close to 1 trillion, and then just let it run.
    for target_fuel_amt in int_stream(start=1_896_680):
        sum_for_fuel = _calc_ore_required_for_fuel_amount(
            fuel_target=target_fuel_amt,
            material_map=material_map,
        )
        if sum_for_fuel <= 1_000_000_000_000:
            max_fuel_so_far = target_fuel_amt
        else:
            return max_fuel_so_far

    raise ValueError


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

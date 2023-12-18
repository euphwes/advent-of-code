from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from math import prod
from typing import DefaultDict, List, Optional
from uuid import uuid4

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 20
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


class PulseType(Enum):
    LOW = "low"
    HIGH = "high"


@dataclass
class Pulse:
    id: str
    type: PulseType
    originating_module_name: str
    target_module_name: str


class ModuleType(Enum):
    FLIP_FLOP = "flip_flop"
    BROADCAST = "broadcast"
    CONJUNCTION = "conjunction"
    OUTPUT = "output"


@dataclass
class Module:
    type: ModuleType
    name: str
    state: Optional[bool]
    pulse_history: Optional[DefaultDict[str, PulseType]]
    recipient_names: List[str]

    def __str__(self):
        if self.type == ModuleType.FLIP_FLOP:
            state = "on" if self.state is True else "off"
            return f"{self.name}: {state}"

        if self.type == ModuleType.CONJUNCTION:
            assert self.pulse_history is not None
            state = ", ".join(
                f"{name}: {val}" for name, val in self.pulse_history.items()
            )
            return f"{self.name}: {state}"

    def receive_pulse(self, pulse: Pulse) -> List[Pulse]:
        if self.type == ModuleType.BROADCAST:
            return [
                Pulse(
                    id=str(uuid4()),
                    type=pulse.type,
                    originating_module_name=self.name,
                    target_module_name=target,
                )
                for target in self.recipient_names
            ]
        elif self.type == ModuleType.FLIP_FLOP:
            if pulse.type == PulseType.HIGH:
                return []
            else:
                assert self.state is not None
                self.state = not self.state
                next_pulse_type = PulseType.HIGH if self.state else PulseType.LOW
                return [
                    Pulse(
                        id=str(uuid4()),
                        type=next_pulse_type,
                        originating_module_name=self.name,
                        target_module_name=target,
                    )
                    for target in self.recipient_names
                ]
        elif self.type == ModuleType.CONJUNCTION:
            assert self.pulse_history is not None
            self.pulse_history[pulse.originating_module_name] = pulse.type

            next_pulse_type = PulseType.HIGH
            if all(memory == PulseType.HIGH for memory in self.pulse_history.values()):
                next_pulse_type = PulseType.LOW

            return [
                Pulse(
                    id=str(uuid4()),
                    type=next_pulse_type,
                    originating_module_name=self.name,
                    target_module_name=target,
                )
                for target in self.recipient_names
            ]
        elif self.type == ModuleType.OUTPUT:
            return []
        else:
            raise ValueError(self.type)


def _parse_modules(stuff):
    def _get_output_mod():
        return Module(
            type=ModuleType.OUTPUT,
            name=str(uuid4()),
            pulse_history=None,
            recipient_names=[],
            state=None,
        )

    modules_by_name = defaultdict(_get_output_mod)

    for line in stuff:
        if line.startswith("broadcaster"):
            raw_children = line.split(" -> ")[1].split(", ")

            modules_by_name["broadcaster"] = Module(
                type=ModuleType.BROADCAST,
                name="broadcaster",
                pulse_history=None,
                recipient_names=raw_children,
                state=None,
            )

        elif line.startswith("&"):
            raw_name = line.split(" -> ")[0].replace("&", "")
            raw_children = line.split(" -> ")[1].split(", ")

            modules_by_name[raw_name] = Module(
                type=ModuleType.CONJUNCTION,
                name=raw_name,
                pulse_history=defaultdict(lambda: PulseType.LOW),
                recipient_names=raw_children,
                state=None,
            )

        elif line.startswith("%"):
            raw_name = line.split(" -> ")[0].replace("%", "")
            raw_children = line.split(" -> ")[1].split(", ")

            modules_by_name[raw_name] = Module(
                type=ModuleType.FLIP_FLOP,
                name=raw_name,
                pulse_history=None,
                recipient_names=raw_children,
                state=False,
            )

    return modules_by_name


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    pulse_counts_by_type = {
        # "button": 0,
        PulseType.LOW: 0,
        PulseType.HIGH: 0,
    }
    modules_by_name = _parse_modules(stuff)
    mods = list(modules_by_name.values())
    # for m in modules_by_name.values():
    #     print(m)

    for cmod in [m for m in mods if m.type == ModuleType.CONJUNCTION]:
        assert cmod.pulse_history is not None
        for smod in [s for s in mods if cmod.name in s.recipient_names]:
            cmod.pulse_history[smod.name] = PulseType.LOW

    for _ in range(1000):
        # pulse_counts_by_type["button"] += 1
        pulse_queue = [
            Pulse(
                id=str(uuid4()),
                type=PulseType.LOW,
                originating_module_name="button",
                target_module_name="broadcaster",
            )
        ]

        while pulse_queue:
            pulse = pulse_queue.pop(0)
            pulse_counts_by_type[pulse.type] += 1
            # print(
            #     f"{pulse.originating_module_name} -{pulse.type.value}-> {pulse.target_module_name}"
            # )

            target_module = modules_by_name[pulse.target_module_name]
            output_pulses = target_module.receive_pulse(pulse)

            pulse_queue.extend(output_pulses)

    return prod(pulse_counts_by_type.values())


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    modules_by_name = _parse_modules(stuff)
    mods = list(modules_by_name.values())
    # for m in modules_by_name.values():
    #     print(m)

    for cmod in [m for m in mods if m.type == ModuleType.CONJUNCTION]:
        assert cmod.pulse_history is not None
        for smod in [s for s in mods if cmod.name in s.recipient_names]:
            cmod.pulse_history[smod.name] = PulseType.LOW

    rx_module_sender = [m for m in mods if "rx" in m.recipient_names][0]
    assert len([m for m in mods if "rx" in m.recipient_names]) == 1

    assert rx_module_sender.pulse_history is not None
    rx_module_sender_senders = list(rx_module_sender.pulse_history.keys())
    senders_hi_emits = {name: [] for name in rx_module_sender_senders}

    for i in int_stream():
        pulse_queue = [
            Pulse(
                id=str(uuid4()),
                type=PulseType.LOW,
                originating_module_name="button",
                target_module_name="broadcaster",
            )
        ]

        while pulse_queue:
            pulse = pulse_queue.pop(0)

            if (
                pulse.originating_module_name in rx_module_sender_senders
                and pulse.type == PulseType.HIGH
            ):
                senders_hi_emits[pulse.originating_module_name].append(i)
                if all(len(emits) >= 2 for emits in senders_hi_emits.values()):
                    num_button_presses = 1
                    for emit in senders_hi_emits.values():
                        num_button_presses *= emit[-1] - emit[-2]
                    return num_button_presses

            target_module = modules_by_name[pulse.target_module_name]
            output_pulses = target_module.receive_pulse(pulse)

            pulse_queue.extend(output_pulses)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

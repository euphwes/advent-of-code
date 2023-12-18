from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from math import prod as mathproduct

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 19
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self):
        return self.x + self.m + self.a + self.s

    @classmethod
    def from_string(cls, string):
        string = string[1:-1]
        x, m, a, s = (int(n[2:]) for n in string.split(","))
        return cls(x, m, a, s)


def _parse_workflows(raw_ws):
    workflows = defaultdict(list)

    def _get_gt_rule(attr_name, value, target_workflow):
        def _gt_rule(x):
            if getattr(x, attr_name) > int(value):
                return target_workflow
            return None

        return _gt_rule

    def _get_lt_rule(attr_name, value, target_workflow):
        def _lt_rule(x):
            if getattr(x, attr_name) < int(value):
                return target_workflow
            return None

        return _lt_rule

    def _get_noop_rule(target_workflow):
        def _noop_rule(x):
            return target_workflow

        return _noop_rule

    for line in raw_ws:
        w_name = line[: line.index("{")]

        raw_rules = line[line.index("{") + 1 : -1].split(",")
        for rule in raw_rules:
            if "<" in rule:
                predicate, target_workflow = rule.split(":")
                attr_name, value = predicate.split("<")
                workflows[w_name].append(
                    _get_lt_rule(attr_name, value, target_workflow)
                )
            elif ">" in rule:
                predicate, target_workflow = rule.split(":")
                attr_name, value = predicate.split(">")
                workflows[w_name].append(
                    _get_gt_rule(attr_name, value, target_workflow)
                )
            else:
                workflows[w_name].append(_get_noop_rule(rule))

    return workflows


def _evaluate_workflow_for_part(workflow, part):
    for rule in workflow:
        result = rule(part)
        if result is not None:
            return result
    raise ValueError("No matching workflow found")


def _evaluate_part(workflows, part):
    current_workflow = "in"

    # print(f"\nEvaluating part {part}...")
    while True:
        result = _evaluate_workflow_for_part(workflows[current_workflow], part)
        if result in "AR":
            # print(result)
            return result
        else:
            # print(f"--> {result}", end=" ")
            current_workflow = result


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    raw_ws = list()
    raw_ns = list()

    while True:
        line = stuff.pop(0)
        if line == "":
            break

        raw_ws.append(line)

    while stuff:
        raw_ns.append(stuff.pop(0))

    workflows = _parse_workflows(raw_ws)
    parts = [Part.from_string(n) for n in raw_ns]

    accepted_parts = list()
    for p in parts:
        result = _evaluate_part(workflows, p)
        if result == "A":
            # print(f"Part {p} is accepted")
            accepted_parts.append(p)

    return sum(p.rating for p in accepted_parts)


# ----------------------------------------------------------------------------------------------


class WorkflowNodeType(Enum):
    PREDICATE = "p"
    RESULT = "r"
    WORKFLOW_ROOT = "root"
    PASSTHROUGH = "pt"


@dataclass
class WorkflowNode:
    raw: str
    name: str
    type: WorkflowNodeType
    clause: Optional[str]
    children: List["WorkflowNode"]


def _parse_workflow_nodes(raw_ws):
    nodes = dict()

    for line in raw_ws:
        workflow_name = line[: line.index("{")]
        raw_clauses = line[line.index("{") + 1 : -1].split(",")

        # Add the workflow root note
        workflow_node = WorkflowNode(
            raw=line,
            name=workflow_name,
            type=WorkflowNodeType.WORKFLOW_ROOT,
            clause=None,
            children=[],
        )
        nodes[workflow_node.name] = workflow_node

        prev_node = workflow_node
        for clause in raw_clauses:
            if ">" in clause or "<" in clause:
                new_node = WorkflowNode(
                    raw=clause,
                    name=workflow_name + ": " + clause,
                    type=WorkflowNodeType.PREDICATE,
                    clause=clause[: clause.index(":")],
                    children=[],
                )

                nodes[new_node.name] = new_node
            elif clause == "R" or clause == "A":
                new_node = WorkflowNode(
                    raw=clause,
                    name=clause,
                    type=WorkflowNodeType.RESULT,
                    clause=clause,
                    children=[],
                )
            else:
                new_node = WorkflowNode(
                    raw=clause,
                    name=workflow_name + ": " + clause,
                    type=WorkflowNodeType.PASSTHROUGH,
                    clause=clause,
                    children=[],
                )
            # add to the dict and as a child of previous node in workflow
            nodes[new_node.name] = new_node
            if prev_node:
                prev_node.children.append(new_node)
            prev_node = new_node

    for node in nodes.values():
        if node.type == WorkflowNodeType.PREDICATE:
            target_workflow = node.raw[node.raw.index(":") + 1 :]
            node.children = [nodes[target_workflow]] + node.children
            # print(f"node {node.name} children are {[n.name for n in node.children]}")
        if node.type == WorkflowNodeType.PASSTHROUGH:
            target_workflow = node.clause
            node.children = [nodes[target_workflow]] + node.children
            # print(f"node {node.name} children are {[n.name for n in node.children]}")

    # when wiring, a predicate should have 2 children (if passes, or not)
    # workflow nodes should have 1 child (first predicate)
    # result nodes should have 0 children
    # print(len(nodes))
    for node in nodes.values():
        # print(f"checking {node.name}")
        if node.type == WorkflowNodeType.RESULT:
            assert len(node.children) == 0
        elif node.type == WorkflowNodeType.WORKFLOW_ROOT:
            assert len(node.children) == 1
            assert node.children[0].type == WorkflowNodeType.PREDICATE
        elif node.type == WorkflowNodeType.PREDICATE:
            assert len(node.children) == 2
        elif node.type == WorkflowNodeType.PASSTHROUGH:
            assert len(node.children) == 1
            assert node.children[0].type == WorkflowNodeType.WORKFLOW_ROOT

    return nodes


def _walk(curr_node, restrictions):
    if curr_node.type == WorkflowNodeType.RESULT:
        if curr_node.clause == "A":
            # print()
            # print(restrictions)

            return mathproduct([p2 - p1 + 1 for p1, p2 in restrictions.values()])

        else:
            return 0

    if curr_node.type in (WorkflowNodeType.PASSTHROUGH, WorkflowNodeType.WORKFLOW_ROOT):
        return _walk(curr_node.children[0], restrictions)

    elif curr_node.type == WorkflowNodeType.PREDICATE:
        r_copy = restrictions.copy()
        r_copy_2 = restrictions.copy()
        clause = curr_node.clause
        if "<" in clause:
            attr_name, value = clause.split("<")
            value = int(value)
            r_copy[attr_name] = (
                r_copy[attr_name][0],
                min(value - 1, r_copy[attr_name][1]),
            )
            r_copy_2[attr_name] = (
                max(value, r_copy_2[attr_name][0]),
                r_copy_2[attr_name][1],
            )

        elif ">" in curr_node.clause:
            attr_name, value = clause.split(">")
            value = int(value)
            r_copy[attr_name] = (
                max(value + 1, r_copy[attr_name][0]),
                r_copy[attr_name][1],
            )
            r_copy_2[attr_name] = (
                r_copy_2[attr_name][0],
                min(value, r_copy_2[attr_name][1]),
            )
        else:
            raise ValueError(f"Predicate: {curr_node.clause}")

        # print(f"after {clause}, options are")
        # from pprint import pprint

        # pprint(r_copy)
        # pprint(r_copy_2)

        return _walk(curr_node.children[0], r_copy) + _walk(
            curr_node.children[1], r_copy_2
        )

    else:
        raise ValueError(curr_node.type)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    raw_ws = list()
    while True:
        line = stuff.pop(0)
        if line == "":
            break
        raw_ws.append(line)
    nodes_by_name = _parse_workflow_nodes(raw_ws)

    restrictions = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }
    return _walk(nodes_by_name["in"], restrictions)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)

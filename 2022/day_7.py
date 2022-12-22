from collections import defaultdict
from copy import copy
from dataclasses import dataclass

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 7
YEAR = 2022

PART_ONE_DESCRIPTION = "total size of directories < 100K in size"
PART_ONE_ANSWER = 1325919

PART_TWO_DESCRIPTION = "size of smallest directory to delete"
PART_TWO_ANSWER = 2050735


@dataclass
class File:
    name: str
    size: int


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = list()
        self.subdirectory_names = list()

    def size(self, dir_map):

        # Start by summing the size of all files in this directory.
        size = sum([f.size for f in self.files])

        # Then for each subdirectory, add its size to the size of this directory.
        for subdir in self.subdirectory_names:
            size += dir_map[subdir].size(dir_map)

        return size


def _v1_get_directory_size_map(terminal_output):
    """First implementation, builds a map of directory path to Directory nodes, which contain
    File nodes and references to other Directory nodes, and size is calculated by the
    Directory."""

    directory_stack = list()
    directory_path_node_map = dict()

    while terminal_output:
        terminal_line = terminal_output.pop(0)

        if terminal_line.startswith("$ cd .."):
            # If we're cd-ing up a level, pop a directory off the stack
            dir_name = directory_stack.pop()

        elif terminal_line.startswith("$ cd "):
            # If we're cd-ing into a directory, add that directory to the stack
            dir_name = terminal_line.replace("$ cd ", "")
            directory_stack.append(dir_name)

            # Also get a tuple representing the full path of the directory, and add a
            # Directory node into the map.
            full_dir_path = tuple(directory_stack)
            directory_path_node_map[full_dir_path] = Directory(name=dir_name)

        elif terminal_line.startswith("$ ls"):
            # If we're listing contents of the the current directory...

            # ... keeping reading subsequent lines until we see another command (starts with $)
            # because the output has stopped.
            while terminal_output and not terminal_output[0].startswith("$"):

                # Read the next child of the current directory
                child = terminal_output.pop(0)

                if child.startswith("dir "):
                    # If the child is a directory, get the full path to that directory
                    child_dir = child.replace("dir ", "")
                    full_child_path = tuple(list(full_dir_path) + [child_dir])

                    # Add it to the subdirectories of the current Directory node.
                    directory_path_node_map[full_dir_path].subdirectory_names.append(
                        full_child_path
                    )

                else:
                    # Otherwise the child is a file, add a File node to the current Directory
                    # node.
                    size, filename = child.split()
                    file = File(name=filename, size=int(size))
                    directory_path_node_map[full_dir_path].files.append(file)

    # Return a map of the directory paths to their total size
    return {
        path: node.size(directory_path_node_map)
        for path, node in directory_path_node_map.items()
    }


def _v2_get_directory_size_map(terminal_output):
    """Second implementation, reads serially from the terminal output, maintaining a stack of
    the full paths of all directories we're in, and every time we read a file, add its size to
    all directories in the stack."""

    directory_stack = list()
    directory_size_map = defaultdict(int)

    for line in terminal_output:

        # Don't need to directly do anything if we're reading `ls` or a directory being listed
        # as `ls` output.
        if line.startswith("dir") or line.startswith("$ ls"):
            continue

        # Navigating up a level? Pop from the stack
        if line == "$ cd ..":
            directory_stack.pop()

        # Navigating down a level? Add the full path to the stack.
        elif line.startswith("$ cd "):
            dir_name = line.replace("$ cd ", "")

            # Get the full path of this directory, which is just this directory one layer deeper
            # than the full path of the current path on the stack.
            if directory_stack:
                full_dir_path = tuple(list(directory_stack[-1]) + [dir_name])
            else:
                full_dir_path = (dir_name,)

            directory_stack.append(full_dir_path)

        # The only option left is that we're reading a file
        else:
            # The size is the first space-delimited piece of that line.
            size = int(line.split()[0])

            # This file is (directly or indirectly) inside each directory currently on the stack
            for path in directory_stack:
                directory_size_map[path] += size

    return directory_size_map


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(terminal_output):

    # Just because I implemented two different solutions for determining directory size, I want
    # to call them both and then vet that they are actually the same.

    directory_path_size_map_v1 = _v1_get_directory_size_map(copy(terminal_output))
    directory_path_size_map_v2 = _v2_get_directory_size_map(copy(terminal_output))
    assert directory_path_size_map_v1 == directory_path_size_map_v2

    candidates = [
        size for size in directory_path_size_map_v2.values() if size < 100_000
    ]

    return sum(candidates)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(terminal_output):

    # Just because I implemented two different solutions for determining directory size, I want
    # to call them both and then vet that they are actually the same.

    directory_path_size_map_v1 = _v1_get_directory_size_map(copy(terminal_output))
    directory_path_size_map_v2 = _v2_get_directory_size_map(copy(terminal_output))
    assert directory_path_size_map_v1 == directory_path_size_map_v2

    used_space = directory_path_size_map_v2[("/",)]
    free_space = 70000000 - used_space

    candidates = list()
    for size in directory_path_size_map_v2.values():
        if free_space + size >= 30000000:
            candidates.append(size)

    return min(candidates)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    terminal_output = get_input(input_file)

    part_one(copy(terminal_output))
    part_two(copy(terminal_output))

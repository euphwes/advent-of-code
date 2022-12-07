from util.decorators import aoc_output_formatter
from util.input import get_input

from dataclasses import dataclass

#---------------------------------------------------------------------------------------------------

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
    def __str__(self):
        return f'File(name={self.name}, size={self.size})'


class Directory:
    def __init__(self, name):
        self.name = name
        self.subdirectory_names = list()
        self.files = list()
        
    def size(self, dir_map):
        running_size = sum([f.size for f in self.files])
        for subdir in self.subdirectory_names:
            running_size += dir_map[subdir].size(dir_map)
        return running_size
        
    def __str__(self):
        return f'Dir(name={self.name}, dirs={[d for d in self.subdirectory_names]}, files={[f.name for f in self.files]})'


@aoc_output_formatter(2022, 7, 1, '')
def part_one(lines):
    dir_name_node_map = dict()
    dir_stack = list()
    
    debug = True
    
    while lines:
        command = lines.pop(0)
        if command.startswith('$ cd ') and not '..' in command:
            dir_name = command.replace('$ cd ', '')
            dir_stack.append(dir_name)
            dir_name_node_map[dir_name] = Directory(name=dir_name)
            
        elif command.startswith('$ cd ') and '..' in command:
            dir_name = dir_stack.pop()
        
        elif command.startswith('$ ls'):
            while lines and not lines[0].startswith('$'):
                child = lines.pop(0)
                if child.startswith('dir '):
                    child_dir = child.replace('dir ', '')
                    dir_name_node_map[dir_name].subdirectory_names.append(child_dir)
                else:
                    size, filename = child.split()
                    size = int(size)
                    dir_name_node_map[dir_name].files.append(File(name=filename, size=size))

    for dir in dir_name_node_map.values():
        print(dir)
    print(dir_name_node_map.keys())
    for dir in dir_name_node_map.values():
        print(f'{dir.name}: {dir.size(dir_name_node_map)}')
        
    for dir in dir_name_node_map.values():
        print(dir)
    
    candidates = list()
    for dir in dir_name_node_map.values():
        size = dir.size(dir_name_node_map)
        if size <= 100000:
            candidates.append(size)
    
    # not 937049, 899654
    return sum(candidates)

@aoc_output_formatter(2022, 7, 2, '')
def part_two(stuff):
    pass

#---------------------------------------------------------------------------------------------------

def run(input_file):

    stuff = get_input(input_file)

    part_one(stuff)
    part_two(stuff)

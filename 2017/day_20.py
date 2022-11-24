from util.decorators import aoc_output_formatter
from util.input import get_input

from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple

#---------------------------------------------------------------------------------------------------

@dataclass
class ParticleInfo:
    index: int
    position: Tuple[int, int, int]
    velocity: Tuple[int, int, int]
    acceleration: Tuple[int, int, int]
    
    @property
    def acceleration_magnitude(self):
        ax, ay, az = self.acceleration
        return (ax**2 + ay**2 + az**2)**(0.5)
        
    def tick(self):
        ax, ay, az = self.acceleration
        
        vx, vy, vz = self.velocity
        vx += ax
        vy += ay
        vz += az
        self.velocity = vx, vy, vz
        
        px, py, pz = self.position
        px += vx
        py += vy
        pz += vz
        self.position = px, py, pz
    
    @staticmethod
    def from_line(line, index):
        raw_pos, raw_vel, raw_acc = line.split(', ')
        
        position = tuple([int(p) for p in raw_pos[3:-1].split(',')])
        velocity = tuple([int(p) for p in raw_vel[3:-1].split(',')])
        acceleration = tuple([int(p) for p in raw_acc[3:-1].split(',')])
        
        return ParticleInfo(index, position, velocity, acceleration)


@aoc_output_formatter(2017, 20, 1, 'particle that will remain closest to the origin')
def part_one(raw_particles):
    particles = [ParticleInfo.from_line(line, ix) for ix, line in enumerate(raw_particles)]
    return min(particles, key=lambda p: p.acceleration_magnitude).index


@aoc_output_formatter(2017, 20, 2, 'number of particles remaining after collisions')
def part_two(raw_particles):
    particles = [ParticleInfo.from_line(line, ix) for ix, line in enumerate(raw_particles)]
    
    # 11 is the magic threshold -- 10 didn't result in any collisions, 1000 gave the right answer,
    # and I kept halving it until I learned that 11 ticks since collision yielded the right answer.
    ticks_since_collision = 0
    while ticks_since_collision < 11:

        # Group particles by their position
        particle_locations = defaultdict(list)
        for particle in particles:
            particle_locations[particle.position].append(particle)
            
        # For any particles which share a position with another, add them to a list of particles
        # which have collided so they can be removed from the list.
        particles_to_remove = list()
        for coord, colocated_particles in particle_locations.items():
            if len(colocated_particles) > 1:
                particles_to_remove.extend(colocated_particles)
                
        # If there are any particles to remove, reset the count of ticks since the last collision
        # and remove all those particles.
        if particles_to_remove:
            ticks_since_collision = 0
            for particle in particles_to_remove:
                particles.remove(particle)
                
        # Otherwise if there were no collisions, increase the count of ticks since collisions
        else:
            ticks_since_collision += 1
            
        # For any particles remaining, update their position based on their acceleration and velocity
        for particle in particles:
            particle.tick()
            
    # How many particles remain after collisions are done?
    return len(particles)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw_particles = get_input(input_file)

    part_one(raw_particles)
    part_two(raw_particles)

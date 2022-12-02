from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

#---------------------------------------------------------------------------------------------------

class Reindeer:
    """ Defines a reindeer, which has a name, can fly at a certain speed for a certain amount of
    time, and then must rest. """

    def __init__(self, input_tokens):
        # Tokens ex: `Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.`
        self.name      = input_tokens[0]
        self.speed     = int(input_tokens[3])
        self.fly_time  = int(input_tokens[6])
        self.rest_time = int(input_tokens[-2])


    def fly(self, total_time):
        """ Simulate the reindeer flying for the specified time, and returns the distance flown. """

        flight_iterator = self.stepwise_fly()

        for _ in range(total_time - 1):
            next(flight_iterator)

        return next(flight_iterator)


    def stepwise_fly(self):
        """ Simulate the reindeer flying one second at a time, yielding the current distance
        traveled at each time step. """

        # Alternate between flying and resting
        distance = 0
        while True:
            for _ in range(self.fly_time):
                distance += self.speed
                yield distance

            for _ in range(self.rest_time):
                yield distance

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 14, 1, "Furthest distance traveled by a reindeer", assert_answer=2660)
def part_one(reindeer, time):
    return max(r.fly(time) for r in reindeer)


@aoc_output_formatter(2015, 14, 2, "Most points obtained by a reindeer", assert_answer=1256)
def part_two(reindeer, time):
    reindeer_points    = {r.name: 0 for r in reindeer}
    reindeer_distances = {r.name: 0 for r in reindeer}
    reindeer_flights   = [(r.name, r.stepwise_fly()) for r in reindeer]

    for _ in range(time):
        for reindeer, flight in reindeer_flights:
            reindeer_distances[reindeer] = next(flight)
        current_winning_distance = max(reindeer_distances.values())
        for reindeer, distance in reindeer_distances.items():
            if distance == current_winning_distance:
                reindeer_points[reindeer] = reindeer_points[reindeer] + 1

    return max(reindeer_points.values())

#---------------------------------------------------------------------------------------------------

def run(input_file):

    # Parse reindeer from the input file
    reindeer = [Reindeer(tokens) for tokens in get_tokenized_input(input_file, ' ')]

    part_one(reindeer, 2503)
    part_two(reindeer, 2503)

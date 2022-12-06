from util.decorators import aoc_output_formatter
from util.input import get_input

from .assembly import evaluate_assembly_v3, AssemblyInstruction

from collections import defaultdict

#---------------------------------------------------------------------------------------------------


@aoc_output_formatter(2017, 23, 1, 'total mul instructions called', assert_answer=3025)
def part_one(instructions):
    for stepwise_mul_count in evaluate_assembly_v3(defaultdict(int), instructions):
        pass
    return stepwise_mul_count


@aoc_output_formatter(2017, 23, 2, 'num composite integers in my input range', assert_answer=915)
def part_two():
    
    # Unaltered instructions
    #
    # set b 57
    # set c b
    # jnz a 2
    # jnz 1 5
    # mul b 100
    # sub b -100000
    # set c b
    # sub c -17000
    # set f 1
    # set d 2
    # set e 2
    # set g d
    # mul g e
    # sub g b
    # jnz g 2
    # set f 0
    # sub e -1
    # set g e
    # sub g b
    # jnz g -8
    # sub d -1
    # set g d
    # sub g b
    # jnz g -13
    # jnz f 2
    # sub h -1
    # set g b
    # sub g c
    # jnz g 2
    # jnz 1 3
    # sub b -17
    # jnz 1 -23

    # Start registers a at 1, to skip debug mode
    a = 1

    # set b 57
    # set c b
    # jnz a 2    a == 1, causing the next line to be skipped
    # jnz 1 5
    # mul b 100
    # sub b -100000
    # set c b
    # sub c -17000
    b = (57 * 100) + 100000
    c = b + 17000
    
    # So in short
    b = 105700
    c = 122700
    
    # Remaining instructions broken into loops
    # set f 1
    # set d 2
        # set e 2
            # set g d
            # mul g e
            # sub g b
            # jnz g 2
            # set f 0
            # sub e -1
            # set g e
            # sub g b
            # jnz g -8
        # sub d -1
        # set g d
        # sub g b
        # jnz g -13
    # jnz f 2
    # sub h -1
    # set g b
    # sub g c
    # jnz g 2
    # jnz 1 3
    # sub b -17
    # jnz 1 -23
    
    # Now let's Python-ify the loops...
    
    """
    # Loop over values of b, starting at b = 105700 (from above)
    # ending at b = 122700 (because g = b - c --> g = 0 and loop will end).
    # incrementing b by 17 each time.
    while True:
        
        # Reset flag `f` which is set in the inner loop if a number is not prime
        f = 1

        # Loop over various values of d
        # Start at d = 2, continues until d == b
        # (because g = d - b --> g = 0 and loop will end)

        d = 2
        
        while g != 0:
           
            # Loop over various values of e
            # Start at e = 2, continues until e == b
            # (because g = e - b --> g = 0 and loop will end)
            #
            # Inside, set f = 0 when b = d * e
            # (** NOTE ** this means b is not prime, because it can be expressed
            # as the product of 2 other numbers)

            e = 2
            
            while g != 0:
                g = (d * e) - b
                if g == 0:
                    f = 0
                e += 1
                g = e - b
                
            d += 1
            g = d - b
        
        if f == 0:
            h += 1
        
        g = b - c
        if g == 0:
            break
        
        b += 17
    """

    # Now let's convert this to more idiomatic Python with ranges, and break out early if
    # we identify a number that is not prime.
    
    """
    # This the register h
    count_not_prime = 0
    
    for b in range(105700, 122700+1, 17):

        # This is the register/flag f.
        # Assume b is prime until we prove otherwise.
        b_is_not_prime = False

        for e in range(2, b+1):
            for d in range(2, b+1):
                # b == d * e, b is not prime. Set the flag (aka set f = 1)
                if d * e == b:
                    b_is_not_prime = True
         
        if b_is_not_prime:
            count_not_prime += 1
     
    return count_not_prime
    """
    
    # But we can implement a better `is_prime` so this doesn't take forever.
    # Final implementation below.
    
    def _is_prime(n):
        for i in range(2, int(n**0.5) + 2):
            if n % i == 0:
                return False
        return True

    # This the register h
    count_not_prime = 0
    
    for b in range(105700, 122700+1, 17):
        if not _is_prime(b):
            count_not_prime += 1

    return count_not_prime

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw_instructions = get_input(input_file)
    instructions = [AssemblyInstruction.from_line(line) for line in raw_instructions]

    part_one(instructions)
    part_two()

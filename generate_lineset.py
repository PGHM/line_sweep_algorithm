import random
import sys
from math import ceil

USAGE = """Usage:
1. parameter: filename to output the random lines
2. parameter: number of lines
3. parameter: approximate length of the line segments
"""

# generate random lines following the rules so that x, y dimensions are 
# equal to the number of lines
def main(output_file, number_of_lines, approx_length):
    
    output = open(output_file, 'w')
    number_of_lines = int(number_of_lines)
    length = int(approx_length)
    fractions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for _ in range(0, number_of_lines):
        start_x = float(random.randint(0, number_of_lines)) + random.choice(fractions)
        start_y = float(random.randint(0, number_of_lines)) + random.choice(fractions)
        end_x = float(random.randint(ceil(start_x), ceil(start_x) + length))
        end_x +=  + random.choice(fractions)
       
        # vertical lines must start from up and end in bottom
        if start_x == end_x:
            end_y = float(random.randint(max(ceil(start_y)-length*2, 0), ceil(start_y)))
            end_y += random.choice(fractions)
        else:
            end_y = float(random.randint(max(ceil(start_y)-length, 0), ceil(start_y) + length))
            end_y += random.choice(fractions)
        output.write("{0},{1},{2},{3}\n".format(start_x, start_y, end_x, end_y))
    output.close()

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 4:
        main(args[1], args[2], args[3])
    else:
        print USAGE

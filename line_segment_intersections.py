import sys
import sweep as s
import naive_intersections as n
from data_structures import PriorityQueue, NeighbourList
from geometry import Point, Line, START_POINT, END_POINT, INTERSECTION_POINT
from time import time

USAGE = """Usage:
1. parameter: filename of the point file
2. parameter: Two options: 
    "s" to use the line sweep algorithm
    "n" to use the naive algorithm
3. parameter: (optional) filename to write results, otherwise will print
"""

def main(filename, algorithm, output_file=None):

    start_time = time()
    if algorithm == "s":
        queue = read_lines_from_filename(filename, "s") 
        intersections, checks = s.calculate_intersections(queue)
    elif algorithm == "n":
        lines = read_lines_from_filename(filename, "n") 
        intersections, checks = n.calculate_intersections(lines)
    else:
        print "Unknown algorithm symbol {0}".format(algorithm)
        return
    end_time = time()
   
    intersections = list(intersections)
    intersections.sort()
    duration = end_time - start_time
    if output_file:
        output = open(output_file, 'w')
        output.write("List of intersections:\n")
        for intersection in intersections:
            output.write(str(intersection))
            output.write("\n")
        output.write("\nFound {0} intersections.\n".format(len(intersections)))
        output.write("Made {0} checks for intersections.\n".format(checks))
        output.write("The search took {0} seconds.\n\n".format(duration))
        output.close()
    else:
        print "List of intersections:"
        for intersection in intersections:
            print intersection
        print "\nFound {0} intersections.".format(len(intersections))
        print "Made {0} checks for intersections.".format(checks)
        print "The search took {0} seconds.\n".format(duration)

def read_lines_from_filename(filename, algorithm):
   
    # Sweep line requires priority queue but the naive one can do with just a
    # list
    if algorithm == "s":
        points = PriorityQueue()
    else:
        lines = []

    try:
        line_file = open(filename, 'r')
    except Exception, e:
        print "Cannot open file named {0}".format(filename)
        return None

    for row in line_file:
        splitted = row.split(',')
        if len(splitted) != 4:
            print "Malformed line: ".format(row)
            continue
        else:
            try:
                start_x = float(splitted[0])
                start_y = float(splitted[1])
                end_x = float(splitted[2])
                end_y = float(splitted[3])
            except Exception, e:
                print "Malformed line: ".format(row)
                continue
            
            line = Line()
            start = Point(start_x, start_y, START_POINT, line)
            end = Point(end_x, end_y, END_POINT, line)
            line.add_points(start, end)

            if algorithm == "s":
                points.add(start)
                points.add(end)
            else:
                lines.append(line)
    
    if algorithm == "s":
        return points
    else:
        return lines

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        main(args[1], args[2])
    elif len(args) == 4:
        main(args[1], args[2], args[3])
    else:
        print USAGE

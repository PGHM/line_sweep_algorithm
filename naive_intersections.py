def calculate_intersections(lines):
    number_of_checks = 0
    intersections = set()
    for i in range(0, len(lines)):
        line = lines[i]
        for j in range(i+1, len(lines)):
            number_of_checks += 1
            other_line = lines[j]
            intersection = line.intersects(other_line)
            if intersection:
                intersections.add(intersection)
    return intersections, number_of_checks 

from data_structures import PriorityQueue, NeighbourList
from geometry import Point, Line, START_POINT, END_POINT, INTERSECTION_POINT

number_of_checks = 0
def calculate_intersections(queue):
    global number_of_checks
    number_of_checks = 0
    intersections = set()
    neighbour_list = NeighbourList()
    while not queue.is_empty():
        point = queue.pop()
        if point.point_type == START_POINT:
            handle_start_point(point, neighbour_list, queue, intersections)
        elif point.point_type == END_POINT:
            handle_end_point(point, neighbour_list, queue, intersections)
        else:
            handle_intersection_point(point, neighbour_list, queue, intersections)

    return intersections, number_of_checks

def handle_start_point(point, neighbour_list, queue, intersections):
    global number_of_checks
    new_neighbours = neighbour_list.add_line(point.line, point.x)
    for neighbour in new_neighbours:
        number_of_checks += 1
        intersection = point.line.intersects(neighbour)
        if intersection:
            intersections.add(intersection)
            queue.add(intersection)

def handle_end_point(point, neighbour_list, queue, intersections):
    global number_of_checks
    new_neighbours = neighbour_list.remove_line(point.line)
    if new_neighbours:
        number_of_checks += 1
        intersection = new_neighbours[0].intersects(new_neighbours[1])
        if intersection:
            intersections.add(intersection)
            queue.add(intersection)

def handle_intersection_point(point, neighbour_list, queue, intersections):
    global number_of_checks
    new_neighbours = neighbour_list.switch_neighbours(
            point.intersecting_lines[0], point.intersecting_lines[1])
    for neighbours in new_neighbours:
        number_of_checks += 1
        intersection = neighbours[0].intersects(neighbours[1])
        if intersection:
            intersections.add(intersection)
            queue.add(intersection)

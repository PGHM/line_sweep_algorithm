END_POINT = 1
START_POINT = 2
INTERSECTION_POINT = 3

class Point:

    # takes two floats as an argument, the type of the point and the line this
    # point belongs to or the intersecting lines if this is an intersection
    # point
    def __init__(self, x, y, point_type, line=None, intersecting_lines=None):
        self.x = x
        self.y = y
        self.point_type = point_type
        self.line = line
        self.intersecting_lines = intersecting_lines

    def __str__(self):
        if self.point_type == START_POINT:
            point_type = "Start"
        elif self.point_type == END_POINT:
            point_type = "End"
        else:
            point_type = "Intersection"
        return "X: {0}, Y: {1}".format(self.x, self.y)

    def __eq__(self, other):
        if (self.x == other.x and
            self.y == other.y and
            self.point_type == other.point_type):
            return True
        else:
            return False

    def __hash__(self):
            return hash(self.x) ^ hash(self.y) ^ hash(self.point_type)

    def __cmp__(self, other):
        if self.x < other.x:
            return -1
        elif self.x == other.x and self.y < other.y:
            return -1
        elif self.x == other.x and self.y == other.y:
            return 0
        else:
            return 1

class Line:

    # we set the points after they have been created because we have to set
    # the line that the points belong to first 
    def __init__(self):
        self.start = None
        self.end = None
        self.k = None
        self.c = None
        self.vertical = False
        self.intersected_lines = []

    # add the start and end point to the line
    def add_points(self, start, end):
        self.start = start
        self.end = end
      
        # we have handle vertical lines as special cases
        if start.x == end.x:
            self.vertical = True
            return

        # calculate the line formula y = kx + c
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        self.k = dy / dx
        self.c = self.start.y - self.k * self.start.x

    def get_intersection_with_sweep_line(self, sweep_x):

        # if the line is vertical, consider the intersection at the start
        # point y
        if self.vertical:
            return self.start.y
        else:
            return self.k * sweep_x + self.c;
    
    # takes a line as a parameter and returns the intersection between this
    # line and the other line or None if there is no intersection
    def intersects(self, other_line):

        # if we have calculated this intersectiong point already
        if other_line in self.intersected_lines:
            return None

        if self.vertical or other_line.vertical:
            return self.handle_vertical_intersection(other_line)

        if self.k - other_line.k == 0:
            return None
        else:
            intersection_x = (other_line.c - self.c) / (self.k - other_line.k)
            intersection_y = self.k * intersection_x + self.c
            
            # check that the intersection point is in the bounding box of both
            # of the lines, otherwise it is out if the line segments and in
            # the lines that the line segments define
            if (not self.inside_bb(intersection_x, intersection_y) or not
                    other_line.inside_bb(intersection_x, intersection_y)):
                return None
            
            self.intersected_lines.append(other_line)
            other_line.intersected_lines.append(self)
            return Point(
                    x=intersection_x, 
                    y=intersection_y,
                    point_type=INTERSECTION_POINT, 
                    intersecting_lines=[self, other_line])
    
    # helper method for intersects, checks if the point is inside the bounding
    # box of this line
    def inside_bb(self, x, y):
        inside_x_range = x <= self.end.x and x >= self.start.x
        if self.k >= 0:
            inside_y_range = y <= self.end.y and y >= self.start.y
        else:
            inside_y_range = y >= self.end.y and y <= self.start.y
        return inside_x_range and inside_y_range 

    def handle_vertical_intersection(self, other_line):

        # if both lines are vertical they have either none, or infinite
        # intersection points, so for the sake of clarity, return None
        if self.vertical and other_line.vertical:
            return None

        # check which of the lines is vertical, assing it to line1
        if self.vertical:
            line1 = self
            line2 = other_line
        else:
            line1 = other_line
            line2 = self
       
        # check if the intersection points y-coordinate is in the vertical
        # lines y-range
        intersection_y = line2.k * line1.start.x + line2.c
        if line1.start.y > line1.end.y:
            if intersection_y >= line1.start.y or intersection_y <= line1.end.y:
                return None
        else:
            if intersection_y <= line1.start.y or intersection_y >= line1.end.y:
                return None

        self.intersected_lines.append(other_line)
        other_line.intersected_lines.append(self)
        return Point(
                x=line1.start.x, 
                y=intersection_y,
                point_type=INTERSECTION_POINT, 
                intersecting_lines=[line1, line2])
        
    def __str__(self):
        return "Line with Start: [{0}, {1}] End: [{2}, {3}]".format(
                self.start.x, self.start.y, self.end.x, self.end.y)

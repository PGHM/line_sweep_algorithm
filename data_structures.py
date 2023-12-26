from geometry import START_POINT

class PriorityQueue:

    def __init__(self):
        self.queue = []

    # Priority is the x coordinate of the point, then y coordinate, then the
    # weight of the point type
    def add(self, new_point):

        # use a form of binary search to find the correct position in the
        # queue, to achieve log(N) insert speed
        start = 0
        end = len(self.queue) - 1
        
        while start <= end:
            middle = (start + end) / 2
            point = self.queue[middle]

            if new_point.x < point.x:
                end = middle - 1
            elif point.x == new_point.x and new_point.y > point.y:
                end = middle - 1
            elif point.x == new_point.x and point.y == new_point.y:
                if new_point.point_type > point.point_type:
                    end = middle - 1
                else:
                    start = middle + 1
            else:
                start = middle + 1
        
        self.queue.insert(start, new_point)

    # Assumes that caller checks if the queue is empty
    def pop(self):
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

class NeighbourList:

    # lines are ordered top y coordinate first
    def __init__(self):
        self.list = []
    
    # inserts line and returs array of possible new neighbours to added line
    def add_line(self, new_line, sweep_x):
        position = 0
        for line in self.list:
            if (new_line.get_intersection_with_sweep_line(sweep_x) >
                line.get_intersection_with_sweep_line(sweep_x)):
                break;
            else:
                position += 1

        self.list.insert(position, new_line)
        new_neighbours = []
        if position > 0:
            new_neighbours.append(self.list[position - 1])
        if position < len(self.list) - 1:
            new_neighbours.append(self.list[position + 1])
        return new_neighbours

    # removes the line and returns tuple of two lines that are new neighbours
    # or None if there were no new neighbours
    def remove_line(self, line):
        index = self.list.index(line)
        self.list.remove(line)
        if index > 0 and index < len(self.list):
            return (self.list[index-1], self.list[index])
        else:
            return None

    # switches the neighbours positions in the queue and returns array of new
    # neighbour pair tuples, if any
    def switch_neighbours(self, line1, line2):
        i = self.list.index(line1)
        i2 = self.list.index(line2)
        if i < i2:
            return self.switch(i, line1, i2, line2)
        else:
            return self.switch(i2, line2, i, line1)

    # helper method for switch neighbours, switches the lines and returns
    # their new neighbours
    def switch(self, i, line1, i2, line2):
        self.list[i] = line2
        self.list[i2] = line1
        
        new_neighbours = []
        if i > 0:
            new_neighbours.append((self.list[i-1], line2)) 
        if i2 < len(self.list) - 1:
            new_neighbours.append((self.list[i2+1], line1))
        return new_neighbours

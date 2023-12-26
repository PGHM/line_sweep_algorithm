import unittest
from geometry import Point, Line, START_POINT, END_POINT, INTERSECTION_POINT
from data_structures import PriorityQueue, NeighbourList

class TestGeometry(unittest.TestCase):

    def test_line(self):
        self.line1 = self.make_test_line(0.0,0.0,2.0,2.0)
        self.assertEqual(self.line1.k, 1.0)
        self.assertEqual(self.line1.c, 0.0)
        self.assertEqual(self.line1.get_intersection_with_sweep_line(1.0),
                1.0)

        self.line2 = self.make_test_line(0.0,2.0,2.0,0.0)
        self.assertEqual(self.line2.k, -1.0)
        self.assertEqual(self.line2.c, 2.0)
        self.assertEqual(self.line2.get_intersection_with_sweep_line(1.0),
                1.0)

        intersection = self.line2.intersects(self.line1)
        self.assertEqual(intersection.x, 1.0)
        self.assertEqual(intersection.y, 1.0)
        
        self.line3 = self.make_test_line(0.0,1.5,2.5,1.5)
        self.assertEqual(self.line3.k, 0.0)
        self.assertEqual(self.line3.c, 1.5)

        intersection = self.line2.intersects(self.line3)
        self.assertEqual(intersection.x, 0.5)
        self.assertEqual(intersection.y, 1.5)
        
        self.line4 = self.make_test_line(0.0,3.0,1.0,2.0)
        intersection = self.line4.intersects(self.line3)
        self.assertEqual(intersection, None)
        
        intersection = self.line4.intersects(self.line2)
        self.assertEqual(intersection, None)
        
        self.line5 = self.make_test_line(1.0,2.0,2.0,3.0)
        intersection = self.line5.intersects(self.line4)
        self.assertEqual(intersection.x, 1.0)
        self.assertEqual(intersection.y, 2.0)
        
        self.line6 = self.make_test_line(0.5,3.0,1.5,2.0)
        intersection = self.line1.intersects(self.line6)
        self.assertEqual(intersection, None)
        
        self.line7 = self.make_test_line(0.0,0.0,0.9999,0.9999)
        intersection = self.line2.intersects(self.line7)
        self.assertEqual(intersection, None)

        # testing vertical lines
        self.line8 = self.make_test_line(1.0,0.0,1.0,3.0)
        self.assertEqual(self.line8.k, None)
        self.assertEqual(self.line8.c, None)
        self.assertTrue(self.line8.vertical)

        self.line9 = self.make_test_line(1.0,4.0,1.0,5.0)
        intersection = self.line8.intersects(self.line9)
        self.assertEqual(intersection, None)

        intersection = self.line2.intersects(self.line8)
        self.assertEqual(intersection.x, 1.0)
        self.assertEqual(intersection.y, 1.0)
        
        intersection = self.line6.intersects(self.line8)
        self.assertEqual(intersection.x, 1.0)
        self.assertEqual(intersection.y, 2.5)
        
        intersection = self.line1.intersects(self.line9)
        self.assertEqual(intersection, None)

        # checking that intersections are calculated only once 
        intersection = self.line2.intersects(self.line3)
        self.assertEqual(intersection, None)
        
        intersection = self.line3.intersects(self.line2)
        self.assertEqual(intersection, None)

        intersection = self.line2.intersects(self.line1)
        self.assertEqual(intersection, None)
        
        intersection = self.line1.intersects(self.line2)
        self.assertEqual(intersection, None)
        
        intersection = self.line2.intersects(self.line8)
        self.assertEqual(intersection, None)
        
        intersection = self.line8.intersects(self.line2)
        self.assertEqual(intersection, None)

    def make_test_line(self, start_x, start_y, end_x, end_y):
        line = Line()
        start = Point(start_x, start_y, START_POINT, line)
        end = Point(end_x, end_y, END_POINT, line)
        line.add_points(start, end)
        return line
    
class TestDataStructures(unittest.TestCase):

    def setUp(self):
        self.line1 = self.make_test_line(0.0,0.0,2.0,2.0)
        self.line2 = self.make_test_line(0.0,2.0,2.0,0.0)
        self.line3 = self.make_test_line(1.0,2.0,2.0,3.0)
        self.line4 = self.make_test_line(0.0,3.0,1.0,2.0)
        self.line5 = self.make_test_line(5.0,0.0,4.0,1.0)
        self.line6 = self.make_test_line(0.0,1.5,2.5,1.5)
        self.line7 = self.make_test_line(0.5,3.0,2.5,1.0)
        
        dummy = Line()
        self.point1 = Point(0.1,0.2, START_POINT, dummy)
        self.point2 = Point(1.0,2.5, START_POINT, dummy)
        self.point3 = Point(0.7,2.5, START_POINT, dummy)
        self.point4 = Point(0.7,2.0, START_POINT, dummy)
        self.point5 = Point(1.0,2.2, END_POINT, dummy)
        self.point6 = Point(1.0,2.2, START_POINT, dummy)
    
    def test_priority_queue(self):
        queue = PriorityQueue()
        queue.add(self.point1)
        queue.add(self.point2)
        queue.add(self.point3)
        queue.add(self.point4)
        queue.add(self.point5)
        queue.add(self.point6)
       
        self.assertEqual(self.point1, queue.pop())
        self.assertEqual(self.point3, queue.pop())
        self.assertEqual(self.point4, queue.pop())
        self.assertEqual(self.point2, queue.pop())
        self.assertEqual(self.point6, queue.pop())
        self.assertEqual(self.point5, queue.pop())
        self.assertTrue(queue.is_empty())
        
        queue.add(self.point5)
        queue.add(self.point3)
        queue.add(self.point1)
        queue.add(self.point4)
        queue.add(self.point2)
        queue.add(self.point6)
        
        self.assertEqual(self.point1, queue.pop())
        self.assertEqual(self.point3, queue.pop())
        self.assertEqual(self.point4, queue.pop())
        self.assertFalse(queue.is_empty())
        
        queue.add(self.point3)
        queue.add(self.point1)
        queue.add(self.point4)
        
        self.assertEqual(self.point1, queue.pop())
        self.assertEqual(self.point3, queue.pop())
        self.assertEqual(self.point4, queue.pop())
        self.assertEqual(self.point2, queue.pop())
        self.assertEqual(self.point6, queue.pop())
        self.assertEqual(self.point5, queue.pop())
        self.assertTrue(queue.is_empty())

    # this test case also simulates the sweep line order of handling things,
    # drawing the lines helps with understanding the correct outcomes
    def test_neighbour_list(self):
        neighbour_list = NeighbourList()
        new_neighbours = neighbour_list.add_line(self.line1, 0)
        self.assertEqual(len(new_neighbours), 0)

        new_neighbours = neighbour_list.add_line(self.line2, 0)
        self.assertEqual(new_neighbours[0], self.line1)
        
        new_neighbours = neighbour_list.add_line(self.line4, 0)
        self.assertEqual(new_neighbours[0], self.line2)
        
        new_neighbours = neighbour_list.add_line(self.line6, 0)
        self.assertEqual(new_neighbours[0], self.line2)
        self.assertEqual(new_neighbours[1], self.line1)

        new_neighbours = neighbour_list.add_line(self.line7, 0.5)
        self.assertEqual(new_neighbours[0], self.line4)

        new_neighbours = neighbour_list.switch_neighbours(self.line2,
                self.line6)
        self.assertEqual(new_neighbours[0][0], self.line4)
        self.assertEqual(new_neighbours[1][0], self.line1)

        new_neighbours = neighbour_list.remove_line(self.line4)
        self.assertEqual(new_neighbours[0], self.line7)
        self.assertEqual(new_neighbours[1], self.line6)

        new_neighbours = neighbour_list.add_line(self.line3, 1.0)
        self.assertEqual(new_neighbours[0], self.line7)
        self.assertEqual(new_neighbours[1], self.line6)

        new_neighbours = neighbour_list.switch_neighbours(self.line1,
                self.line2)
        self.assertEqual(new_neighbours[0][0], self.line6)
          
        new_neighbours = neighbour_list.switch_neighbours(self.line3,
                self.line7)
        self.assertEqual(new_neighbours[0][0], self.line6)

        new_neighbours = neighbour_list.switch_neighbours(self.line6,
                self.line1)
        self.assertEqual(new_neighbours[0][0], self.line7)
        self.assertEqual(new_neighbours[1][0], self.line2)
        
        new_neighbours = neighbour_list.switch_neighbours(self.line7,
                self.line1)
        self.assertEqual(new_neighbours[0][0], self.line3)
        self.assertEqual(new_neighbours[1][0], self.line6)

        new_neighbours = neighbour_list.remove_line(self.line3)
        self.assertEqual(new_neighbours, None)

        new_neighbours = neighbour_list.remove_line(self.line1)
        self.assertEqual(new_neighbours, None)

        new_neighbours = neighbour_list.switch_neighbours(self.line7,
                self.line6)
        self.assertEqual(new_neighbours[0][0], self.line2)

        new_neighbours = neighbour_list.remove_line(self.line2)
        self.assertEqual(new_neighbours, None)

        new_neighbours = neighbour_list.remove_line(self.line6)
        self.assertEqual(new_neighbours, None)
    
        new_neighbours = neighbour_list.remove_line(self.line7)
        self.assertEqual(new_neighbours, None)

        new_neighbours = neighbour_list.add_line(self.line5, 4.0)
        self.assertEqual(len(new_neighbours), 0)
        
        new_neighbours = neighbour_list.remove_line(self.line5)
        self.assertEqual(new_neighbours, None)

        self.assertTrue(len(neighbour_list.list) == 0)

    def make_test_line(self, start_x, start_y, end_x, end_y):
        line = Line()
        start = Point(start_x, start_y, START_POINT, line)
        end = Point(end_x, end_y, END_POINT, line)
        line.add_points(start, end)
        return line

if __name__ == '__main__':
    unittest.main()

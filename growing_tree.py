"""
Generate perfect mazes using the growing tree algorithm
"""

import random
import sys

from utils import Point, Box


class GrowingTreeMaze(object):

    """Store and display growing tree mazes"""

    def __init__(self, x_max, y_max):
        """Initialize the "empty" map matrix, growing parameters

        :param height: Display height of the finished maze
        :param width: Display width of the finished maze

        """
        if x_max % 2:
            self._x_max = x_max
        else:
            self._x_max = x_max + 1
        if y_max % 2:
            self._y_max = y_max
        else:
            self._y_max = y_max + 1
        # We'll be drawing the walls as full cells, so we effectively only have
        # half (well, half in each direction, so a quarter) of the visible
        # space to work with.
        self._matrix = []
        for _ in range(self._y_max // 2):
            row = []
            for _ in range(self._x_max // 2):
                # False indicates a wall, True indicates is_passable
                row.append(Box(False, False, False, False))
            self._matrix.append(row)

    def carve(self, point, direction):
        print "Carving %s from %s" % (direction, repr(point))
        # As a convenient side effect, this will raise an index error if we try
        # to carve off the grid
        if direction == 'U':
            self._matrix[point.y][point.x].top = True
            self._matrix[point.y - 1][point.x].bottom = True
        elif direction == 'D':
            self._matrix[point.y][point.x].bottom = True
            self._matrix[point.y + 1][point.x].top = True
        elif direction == 'L':
            self._matrix[point.y][point.x].left = True
            self._matrix[point.y][point.x - 1].right = True
        elif direction == 'R':
            self._matrix[point.y][point.x].right = True
            self._matrix[point.y][point.x + 1].left = True

    def get_walls(self, point):
        """Interface between x,y points and row-major grid
        """
        if point.y < 0 or point.x < 0:
            raise IndexError
        return self._matrix[point.y][point.x]

    def get_uncarved_neighbors(self, point):
        """Return a list of directions (suitable for input into carve) of
        cells neighboring the given point that have not been carved.
        """
        neighbors = []
        cases = (
                ('U', Point(point.x, point.y - 1)),
                ('D', Point(point.x, point.y + 1)),
                ('L', Point(point.x - 1, point.y)),
                ('R', Point(point.x + 1, point.y)),
        )
        for direction, neighbor in cases:
            try:
                walls = self.get_walls(neighbor)
            except IndexError:
                continue
            if not any(walls):
                neighbors.append((direction, neighbor))
        return neighbors

    def generate(self):
        """Generate the maze
        """
        start_x = random.randint(0, (self._x_max // 2) - 1)
        start_y = random.randint(0, (self._y_max // 2) - 1)
        to_carve_list = [Point(start_x, start_y)]
        while to_carve_list:
            point = random.choice(to_carve_list)
            neighbors = self.get_uncarved_neighbors(point)
            if len(neighbors) == 0:
                to_carve_list.remove(point)
                continue
            direction, next_point = random.choice(neighbors)
            self.carve(point, direction)
            to_carve_list.append(next_point)

    def __str__(self):
        # import pprint
        # pprint.pprint(self._matrix)
        display_matrix = [['#' for _ in range(self._x_max)]
                          for _ in range(self._y_max)]
        for wall_y, row in enumerate(self._matrix):
            for wall_x, cell in enumerate(row):
                display_matrix[wall_y * 2 + 1][wall_x * 2 + 1] = '.'
                if cell.top:
                    display_matrix[wall_y * 2][wall_x * 2 + 1] = '.'
                if cell.left:
                    display_matrix[wall_y * 2 + 1][wall_x * 2] = '.'
        retval = ''
        for row in display_matrix:
            for cel in row:
                retval += cel
            retval += '\n'
        return retval


def main():
    """Driver function
    """
    if len(sys.argv) == 2:
        seed = int(sys.argv[1])
    else:
        seed = random.randint(0, sys.maxint)
    print "Seeding with %s" % seed
    random.seed(seed)
    maze = GrowingTreeMaze(50, 50)
    maze.generate()
    print maze

if __name__ == '__main__':
    main()

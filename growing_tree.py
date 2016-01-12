"""
Generate perfect mazes using the growing tree algorithm
"""

import random
import sys

from utils import Point, Box
from walled_matrix import WalledMatrix


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
        self._matrix = WalledMatrix(self._x_max // 2, self._y_max // 2)

    @property
    def matrix(self):
        return self._matrix

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
                walls = self._matrix.get_walls(neighbor)
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
            self._matrix.carve(point, direction)
            to_carve_list.append(next_point)

    def __str__(self):
        return str(self._matrix)


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

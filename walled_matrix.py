"""
Class for storing and drawing a matrix made up of cells with up to four walls
"""

from utils import Point, Box

class WalledMatrix(object):

    """Store a matix of four walled boxes"""

    def __init__(self, x_max, y_max):
        """Create a matrix of the given size.  Note that print size will be
        twice as larg in either direction, for the conversion to tiles

        :param x_max: x dimension
        :param y_max: y dimension

        """
        self._x_max = x_max
        self._y_max = y_max
        self._matrix = []
        for _ in range(self._y_max):
            row = []
            for _ in range(self._x_max):
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

    def __str__(self):
        # import pprint
        # pprint.pprint(self._matrix)
        display_matrix = [['#' for _ in range(self._x_max * 2 + 1)]
                          for _ in range(self._y_max * 2 + 1)]
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



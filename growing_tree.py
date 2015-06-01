"""
Generate perfect mazes using the growing tree algorithm
"""

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
        for i in range(self._y_max // 2):
            row = []
            for j in range(self._x_max // 2):
                # False indicates a wall, True indicates is_passable
                row.append(Box(False, False, False, False))
            self._matrix.append(row)

    def get_walls(self, point):
        raise NotImplementedError

    def carve(self, point, direction):
        raise NotImplementedError

    def generate(self):
        """Generate the maze
        """
        # Hard code for now so I can test dispaly
        self._matrix[0][0].right = True
        self._matrix[0][1].left = True
        self._matrix[0][1].bottom = True
        self._matrix[0][1].right = True
        self._matrix[0][2].left = True

        self._matrix[1][0].bottom = True
        self._matrix[1][1].top = True
        self._matrix[1][1].right = True
        self._matrix[1][2].bottom = True
        self._matrix[1][2].left = True

        self._matrix[2][0].top = True
        self._matrix[2][0].right = True
        self._matrix[2][1].left = True
        self._matrix[2][1].right = True
        self._matrix[2][2].top = True
        self._matrix[2][2].left = True

    def __str__(self):
        display_matrix = [['#' for _ in range(self._x_max)] for _ in range(self._y_max)]
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
    maze = GrowingTreeMaze(7, 7)
    maze.generate()
    print maze

if __name__ == '__main__':
    main()

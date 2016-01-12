import random
import sys
import copy

from utils import Point, Box
from walled_matrix import WalledMatrix
from growing_tree import GrowingTreeMaze
class BraidMaze(object):

    """Convert a perfect maze into a braided maze"""

    def __init__(self, x_max, y_max):
        self._x_max = x_max
        self._y_max = y_max
        gt = GrowingTreeMaze(x_max, y_max)
        gt.generate()
        self._matrix = gt.matrix

    def generate(self):
        """Remove dead ends from the maze
        """
        print self._matrix
        for point, cell in self._matrix:
            walls = zip(('U', 'L', 'D', 'R'), cell)
            blocked = [x for x in walls if not x[1]]
            if len(blocked) < 3:
                # we have more than one exit, this isn't a dead end and we
                # don't need to do anything
                continue
            print "***"
            print "%s: %s" % (blocked, len(blocked))
            random.shuffle(blocked)
            while(blocked):
                try:
                    self._matrix.carve(point, blocked.pop()[0])
                except IndexError:
                    continue
                break

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
    maze = BraidMaze(50, 50)
    maze.generate()
    print maze

if __name__ == '__main__':
    main()

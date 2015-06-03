"""
Assorted utility classes for working with mazes
"""
from collections import namedtuple


# Box = namedtuple('Box', ['top', 'left', 'bottom', 'right'])
class Box(object):

    """Docstring for Box. """

    def __init__(self, top, left, bottom, right):
        """TODO: to be defined.

        :param top: TODO
        :param left: TODO
        :param bottom: TODO
        :param right: TODO

        """
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def __str__(self):
        return ("Box(top=%s, left=%s, bottom=%s, right=%s)" %
               (self.top, self.left, self.bottom, self.right))

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return 4

    def __iter__(self):
        yield self.top
        yield self.left
        yield self.bottom
        yield self.right

Point = namedtuple('Point', ['x', 'y'])

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

Point = namedtuple('Point', ['x', 'y'])

"""
Generate dungeon using BSP algorithm
"""

import random
import sys

from utils import Box, Point


class Dungeon(object):
    """
    Driver object for building the dungeon
    """

    def __init__(self, x_max, y_max, room_min=3, edge_min=1, max_depth=4):
        self.x_max = x_max
        self.y_max = y_max
        self.room_min = room_min
        self.edge_min = edge_min
        self.max_depth = max_depth
        self.matrix = [['#' for _ in range(x_max)] for _ in range(y_max)]

    def get_tile(self, point):
        """Wrap access to the internal map matrix
        """
        print "Getting tile for %s" % repr(point)
        return self.matrix[point.y][point.x]

    def set_tile(self, point, glyph="."):
        """Wrap access to the internal map matrix
        """
        self.matrix[point.y][point.x] = glyph

    def __str__(self):
        retval = ''
        for row in self.matrix:
            for cel in row:
                retval += cel
            retval += '\n'
        return retval

    def mk_room(self, bounding_box):
        """Make a room that fits within the given box
        """
        if (bounding_box.top + self.edge_min + self.room_min
                > bounding_box.bottom):
            raise ValueError("Region too small to make room")
        if (bounding_box.left + self.edge_min + self.room_min
                > bounding_box.right):
            raise ValueError("Region too small to make room")
        h_max = bounding_box.bottom - bounding_box.top - self.edge_min
        w_max = bounding_box.right - bounding_box.left - self.edge_min
        height = random.randint(self.room_min, h_max)
        width = random.randint(self.room_min, w_max)

        # we now have a room height and width that fit within our bounding box.
        # Just need to decide where to put the top left corner
        y_start = random.randint(bounding_box.top + self.edge_min,
                                 bounding_box.bottom - height)
        x_start = random.randint(bounding_box.left + self.edge_min,
                                 bounding_box.right - width)
        room = Box(y_start, x_start, y_start + height - 1, x_start + width - 1)
        for i in range(y_start, y_start + height):
            for j in range(x_start, x_start + width):
                self.set_tile(Point(j, i))
        return room

    def line_connection(self, room_1, room_2, split, is_vertical):
        """Connect two sections of the maze using a straight line.  The
        corridor will extend straight up and down (or left and right, depending
        on the :param is_vertical: setting) until it hits a non-wall tile.
        """
        if is_vertical:
            # Vertical splitting need a horizontal (i.e. constant Y) connecting
            # line.  The conecting line is always perpendicular to the
            # splitting line.
            overlap_top = max(room_1.top, room_2.top)
            overlap_bottom = min(room_1.bottom, room_2.bottom)
            print "ot: %s, ob: %s" % (overlap_top, overlap_bottom)
            if overlap_bottom < overlap_top:
                raise ValueError("No vertical overlap between %s and %s"
                                 % (room_1, room_2))
            start_y = random.randint(overlap_top, overlap_bottom)
            print "picked vertical overlap point %s between %s and %s" % (
                start_y, room_1, room_2)
            x = split
            while self.get_tile(Point(x, start_y)) == '#':
                self.set_tile(Point(x, start_y), glyph='-')
                x -= 1
            x = split + 1
            while self.get_tile(Point(x, start_y)) == '#':
                self.set_tile(Point(x, start_y), glyph='-')
                x += 1
        else:
            # Horizontal splitting line need a vertical (i.e. constant X)
            # connecting line.  The connecting line is always perpendicular to
            # the splitting line
            overlap_left = max(room_1.left, room_2.left)
            overlap_right = min(room_1.right, room_2.right)
            print "ol: %s, or: %s" % (overlap_left, overlap_right)
            if overlap_right < overlap_left:
                raise ValueError("No horizontal overlap between %s and %s"
                                 % (room_1, room_2))
            start_x = random.randint(overlap_left, overlap_right)
            print("picked horizontal overlap point %s between %s and %s"
                  % (start_x, room_1, room_2))
            y = split
            while self.get_tile(Point(start_x, y)) == '#':
                self.set_tile(Point(start_x, y), glyph='|')
                y -= 1
            y = split + 1
            while self.get_tile(Point(start_x, y)) == '#':
                self.set_tile(Point(start_x, y), glyph='|')
                y += 1

    def bend_connection(self, room_1, room_2):
        """Make a connection with a right angle in it - used when the two
        rooms don't share a facing side
        """
        bend_point = Point(random.randint(room_1.left, room_1.right),
                           random.randint(room_2.top, room_2.bottom))
        if room_1.bottom < room_2.top:
            draw_point = bend_point
            while self.get_tile(draw_point) == '#':
                self.set_tile(draw_point, glyph='|')
                draw_point = Point(draw_point.x, draw_point.y-1)
        else:
            draw_point = bend_point
            while self.get_tile(draw_point) == '#':
                self.set_tile(draw_point, glyph='|')
                draw_point = Point(draw_point.x, draw_point.y+1)
        if room_1.left < room_2.right:
            # Move off our starting point, so we start on a wall
            draw_point = Point(bend_point.x+1, bend_point.y)
            while self.get_tile(draw_point) == '#':
                self.set_tile(draw_point, glyph='-')
                draw_point = Point(draw_point.x+1, draw_point.y)
        else:
            # Move off our starting point, so we start on a wall
            draw_point = Point(bend_point.x-1, bend_point.y)
            while self.get_tile(draw_point) == '#':
                self.set_tile(draw_point, glyph='-')
                draw_point = Point(draw_point.x-1, draw_point.y)

    def mk_dungeon(self, bounding_box, depth=0):
        """Recursively generate the dungeon, building rooms as we go down and
        connecting them as we go up
        """
        print "%s" % repr(bounding_box)
        edge_buffer = self.edge_min + self.room_min
        room = None
        if ((depth >= self.max_depth)
                or (bounding_box.top + edge_buffer
                    > bounding_box.bottom - edge_buffer)
                or (bounding_box.left + edge_buffer
                    > bounding_box.right - edge_buffer)):
            room = self.mk_room(bounding_box)
            return room

        is_vertical = bool(random.randint(0, 1))
        if is_vertical:
            split = random.randint(bounding_box.left + edge_buffer,
                                   bounding_box.right - edge_buffer)
            box_1 = Box(bounding_box.top, bounding_box.left,
                        bounding_box.bottom, split)
            box_2 = Box(bounding_box.top, split, bounding_box.bottom,
                        bounding_box.right)
        else:
            # horizontal split
            split = random.randint(bounding_box.top + edge_buffer,
                                   bounding_box.bottom - edge_buffer)
            box_1 = Box(bounding_box.top, bounding_box.left, split,
                        bounding_box.right)
            box_2 = Box(split, bounding_box.left, bounding_box.bottom,
                        bounding_box.right)
        # Room 2 will always be down or right from room 1
        room_1 = self.mk_dungeon(box_1, depth + 1)
        room_2 = self.mk_dungeon(box_2, depth + 1)

        # Now we have two "rooms" (which may be sub-rooms connected by a
        # corridor), and we need to connect them.

        # First see if they share an edge

        # print self
        try:
            self.line_connection(room_1, room_2, split, is_vertical)
        except ValueError:
            self.bend_connection(room_1, room_2)
        # print self
        return Box(
            min(room_1.top, room_2.top),
            min(room_1.left, room_2.left),
            max(room_1.bottom, room_2.bottom),
            max(room_1.right, room_2.right)
        )


def main():
    if len(sys.argv) == 2:
        seed = int(sys.argv[1])
    else:
        seed = random.randint(0, sys.maxint)
    print "Seeding with %s" % seed
    random.seed(seed)
    dungeon = Dungeon(50, 50, max_depth=6)
    dungeon.mk_dungeon(Box(0, 0, 49, 49))
    print dungeon

if __name__ == '__main__':
    main()

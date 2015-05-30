"""
Generate dungeon using BSP algorithm
"""

import random
import sys
from collections import namedtuple


Box = namedtuple('Box', ['top', 'left', 'bottom', 'right'])


class Dungeon(object):
    """
    Driver object for building the dungeon
    """

    def __init__(self, width, height, room_min=3, edge_min=1, max_depth=4):
        self.width = width
        self.height = height
        self.room_min = room_min
        self.edge_min = edge_min
        self.max_depth = max_depth
        self.matrix = [['#' for _ in range(width)] for _ in range(height)]

    def get_tile(self, width, height):
        """Wrap access to the internal map matrix
        """
        return self.matrix[height][width]

    def set_tile(self, width, height, glyph="."):
        """Wrap access to the internal map matrix
        """
        self.matrix[height][width] = glyph

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
        v_start = random.randint(bounding_box.top + self.edge_min,
                                 bounding_box.bottom - height)
        h_start = random.randint(bounding_box.left + self.edge_min,
                                 bounding_box.right - width)
        room = Box(v_start, h_start, v_start + height - 1, h_start + width - 1)
        for i in range(v_start, v_start + height):
            for j in range(h_start, h_start + width):
                self.set_tile(j, i)
        return room

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
            tries = 0
            while tries < 3:
                try:
                    room = self.mk_room(bounding_box)
                except ValueError:
                    tries += 1
                    room = None
                else:
                    break
            if tries == 3:
                print "Gave up trying to make a room"
            return room

        split_dir = random.randint(0, 1)
        if split_dir:
            print "splitting horizontally"
            # horizontal split
            split = random.randint(bounding_box.top + edge_buffer,
                                   bounding_box.bottom - edge_buffer)
            box_1 = Box(bounding_box.top, bounding_box.left, split,
                        bounding_box.right)
            box_2 = Box(split, bounding_box.left, bounding_box.bottom,
                        bounding_box.right)
        else:
            print "splitting vertically"
            split = random.randint(bounding_box.left + edge_buffer,
                                   bounding_box.right - edge_buffer)
            box_1 = Box(bounding_box.top, bounding_box.left,
                        bounding_box.bottom, split)
            box_2 = Box(bounding_box.top, split, bounding_box.bottom,
                        bounding_box.right)

        # Room 2 will always be down or right from room 1
        room_1 = self.mk_dungeon(box_1, depth + 1)
        room_2 = self.mk_dungeon(box_2, depth + 1)

        # Now we have two "rooms" (which may be sub-rooms connected by a
        # corridor), and we need to connect them.

        # First see if they share an edge

        # print self
        # TODO: refactor this - two if clauses are basically the same, just
        # top/bottom and left/right are swapped.  Named tuple implementation
        # _should_ make it easy to parameterize that.
        if split_dir:
            overlap_left = max(room_1.left, room_2.left)
            overlap_right = min(room_1.right, room_2.right)
            print "ol: %s, or: %s" % (overlap_left, overlap_right)
            if overlap_right >= overlap_left:
                corridor_col = random.randint(overlap_left, overlap_right)
                print("picked horizontal overlap point %s between %s and %s"
                      % (corridor_col, room_1, room_2))
                started = False
                start = room_1.bottom
                while self.get_tile(corridor_col, start) == "#":
                    start -= 1
                end = room_2.top
                while self.get_tile(corridor_col, end) == "#":
                    end += 1
                for i in range(start, end):
                    if self.get_tile(corridor_col, i) == '#':
                        started = True
                        self.set_tile(corridor_col, i, "|")
                    elif started:
                        # If we started drawing and now hit a non-wall, we're
                        # done
                        break
            else:
                print("No horizontal overlap between %s and %s"
                      % (room_1, room_2))
        else:
            overlap_top = max(room_1.top, room_2.top)
            overlap_bottom = min(room_1.bottom, room_2.bottom)
            print "ot: %s, ob: %s" % (overlap_top, overlap_bottom)
            if overlap_bottom >= overlap_top:
                corridor_row = random.randint(overlap_top, overlap_bottom)
                print "picked vertical overlap point %s between %s and %s" % (
                    corridor_row, room_1, room_2)
                started = False
                # rooms may be a compound box, in which case room_1.right
                # doesn't border an open tile.  To correct for this, move the
                # start left until we find a non-wall tile.
                start = room_1.right
                while self.get_tile(start, corridor_row) == "#":
                    start -= 1
                end = room_2.left
                while self.get_tile(end, corridor_row) == "#":
                    end += 1
                for i in range(start, end):
                    if self.get_tile(i, corridor_row) == '#':
                        started = True
                        self.set_tile(i, corridor_row, "-")
                    elif started:
                        # If we started drawing and now hit a non-wall, we're
                        # done
                        break
            else:
                print("No vertical overlap between %s and %s"
                      % (room_1, room_2))
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

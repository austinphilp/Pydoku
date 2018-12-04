from constants import BLANK_SPACE_CHAR


class Square(object):
    possibilities = set()
    x = 0
    y = 0

    @property
    def is_solved(self):
        return len(self.possibilities) == 1

    @property
    def value(self):
        return next(iter(self.possibilities)) if self.is_solved else None

    def assign_val(self, val):
        if val != BLANK_SPACE_CHAR:
            self.possibilities = set([val])

    def is_valid(self):
        return len(self.possibilities) > 0

    def eliminate_possibility(self, num):
        if num is None:
            return False
        previouslySolved = self.is_solved
        self.possibilities.discard(num)
        return self.is_solved and not previouslySolved

    def get_coord(self):
        return (self.x, self.y)

    def __init__(self, x, y, val):
        self.possibilities = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.x = x
        self.y = y
        self.assign_val(val)

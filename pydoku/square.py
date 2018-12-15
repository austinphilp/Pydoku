from constants import BLANK_SPACE_CHAR


class Square(object):
    def __init__(self, x, y, val):
        self.possibilities = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.x, self.y = x, y
        self.value = val

    @property
    def coord(self):
        return (self.x, self.y)

    @property
    def is_solved(self):
        return len(self.possibilities) == 1

    @property
    def value(self):
        return next(iter(self.possibilities)) if self.is_solved else None

    @value.setter
    def value(self, val):
        if val != BLANK_SPACE_CHAR:
            self.possibilities = set([val])

    @property
    def is_valid(self):
        return len(self.possibilities) > 0

    def remove_possibility(self, num):
        if num in self.possibilities:
            self.possibilities.discard(num)
            return self.is_solved
        return False

import constants


class Square(object):
    possibilities = set()
    x = 0
    y = 0

    @property
    def is_solved(self):
        return self.number_of_possibilities() == 1

    @property
    def value(self):
        return self.active_possibilities()[0] if self.is_solved else None

    def number_of_possibilities(self):
        return len(self.active_possibilities())

    def active_possibilities(self):
        return [x for x in self.possibilities if x is not None]

    def assign_val(self, val):
        if val != constants.BLANK_SPACE_CHAR:
            for i in range(0, constants.SUDOKU_GRID_SIZE):
                if self.possibilities[i] != val:
                    self.possibilities[i] = None

    def is_valid(self):
        return self.number_of_possibilities() > 0

    def eliminate_possibility(self, num):
        if num is None:
            return False
        previouslySolved = self.is_solved
        self.possibilities[num-1] = None
        return self.is_solved and not previouslySolved

    def get_coord(self):
        return (self.x, self.y)

    def __init__(self, x, y, val):
        self.possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.x = x
        self.y = y
        self.assign_val(val)

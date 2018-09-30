import constants


class Square(object):
    possibilities = []
    x = 0
    y = 0

    def isSolved(self):
        return self.numberOfPossibilities() == 1

    def numberOfPossibilities(self):
        return len(self.activePossibilities())

    def activePossibilities(self):
        return [x for x in self.possibilities if x is not None]

    def getValue(self):
        if not self.isSolved():
            return None
        else:
            return [x for x in self.possibilities if x is not None][0]

    def assignVal(self, val):
        if val != constants.BLANK_SPACE_CHAR:
            for i in range(0, constants.SUDOKU_GRID_SIZE):
                if self.possibilities[i] != val:
                    self.possibilities[i] = None

    def isValid(self):
        return self.numberOfPossibilities() > 0

    def eliminatePossibility(self, num):
        if num is None:
            return False
        previouslySolved = self.isSolved()
        self.possibilities[num-1] = None
        return self.isSolved() and not previouslySolved

    def getPossibilitiesString(self):
        return ''.join(str(num) for num in self.activePossibilities())

    def getCoord(self):
        return (self.x, self.y)

    def __init__(self, x, y, val):
        self.possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.x = x
        self.y = y
        self.assignVal(val)

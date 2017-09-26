import sys
from copy import deepcopy
from copy import copy
from time import sleep

class Square:
    possibilities = []
    x = 0
    y = 0

    def isSolved(self):
        return self.numberOfPossibilities() == 1

    def numberOfPossibilities(self):
        return len(self.activePossibilities())
        
    def activePossibilities(self):
        return [x for x in self.possibilities if x != None]

    def getValue(self):
        if not self.isSolved():
            return None 
        else:
            return [x for x in self.possibilities if x != None][0]

    def assignVal(self, val):
        if val > 0:
            for i in range(0,9):
                if self.possibilities[i] != val:
                    self.possibilities[i] = None

    def addPosibility(self, val):
        self.possibilities[val-1] = val
        return self.isSolved()

    def isValid(self):
        return self.numberOfPossibilities() > 0

    def eliminatePossibility(self, num):
        if num == None: return False
        previouslySolved = self.isSolved()
        self.possibilities[num-1] = None
        return self.isSolved() and not previouslySolved

    def getPossibilitiesString(self):
        return ''.join(str(num) for num in self.activePossibilities())

    def setCoord(self, x, y): 
        self.x = x
        self.y = y

    def __init__(self):
        self.possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y

    def __eq__(self, other):
        return not slef.__eq__(other)


class Grid:
    Squares = []
    
    @staticmethod
    def Solve(grid):
        if all(square.isSolved() for square in flattenArray(deepcopy(grid.Squares))):
            return grid
        if not grid.SquaresAreValid():
            return None

        square = grid.getMostSolvedSquare()
        row, col = square.x, square.y
        for possibility in square.activePossibilities():
            grid.display()
            backupSquares = deepcopy(grid.Squares)
            grid.Squares[row][col].assignVal(possibility)
            grid.smartElimination()
            grid.display()
            result = Grid.Solve(grid)
            if result is not None:
                return result
            else:
                grid.Squares  = backupSquares
        return None

    def getMostSolvedSquare(self):
        minVal = 9
        minSquare = None
        for row in range(0,9):
            for col in range(0,9):
                if not self.Squares[row][col].isSolved():
                    if self.Squares[row][col].numberOfPossibilities() < minVal:
                        minSquare = self.Squares[row][col]
                        minVal = self.Squares[row][col].numberOfPossibilities()
        return minSquare

    def smartElimination(self):
        solved = [square for square in flattenArray(self.Squares) if square.isSolved()]
        while len(solved) > 0:
            square = solved.pop(0)
            solved += Grid.RemovePossibilityForRow( self.Squares, square )
            solved += Grid.RemovePossibilityForCol( self.Squares, square )
            solved += Grid.RemovePossibilityForSubGrid( self.Squares, square )

    def SquaresAreValid(self):
        for row in range(0,9):
            for col in range(0,9):
                if not self.Squares[row][col].isValid():
                    print "NOT VALID"
                    return False
        return True

    @staticmethod
    def RemovePossibilityForRow(squares, square):
        solved = []
        row = square.x
        for col in range(0,9):
            if not col == square.y:
                if squares[row][col].eliminatePossibility(squares[square.x][square.y].getValue()):
                    if not squares[row][col].isValid(): 
                        print "FOUND INVALID"
                        return None
                    else:
                        solved.append(deepcopy(squares[row][col]))
        return solved

    @staticmethod
    def RemovePossibilityForCol(squares, square):
        solved = []
        col = square.y
        for row in range(0,9):
            if not squares[row][col].x == square.x:
                if squares[row][col].eliminatePossibility(squares[square.x][square.y].getValue()):
                    if not squares[row][col].isValid(): 
                        print "FOUND INVALID"
                        return None
                    else:
                        solved.append(deepcopy(squares[row][col]))
        return solved

    @staticmethod
    def RemovePossibilityForSubGrid(squares, square):
        solved = []
        if square.getValue() == None:
            return 
        for row in range((square.x/3)*3, ((square.x/3)*3)+3):
            for col in range((square.y/3)*3, ((square.y/3)*3)+3):
                if row != square.x and col != square.y:
                    if squares[row][col].eliminatePossibility(squares[square.x][square.y].getValue()):
                        if not squares[row][col].isValid(): 
                            print "FOUND INVALID"
                            return None
                        else:
                            solved.append(deepcopy(squares[row][col]))
        return solved

    def bruteForce(self): 
        squares = Grid.GetCorrectSquares(deepcopy(self.Squares))
        Grid.Display(squares)
        self.Squares = squares

    def display(self):
        Grid.Display(self.Squares)

    @staticmethod
    def Display(squares):
        print "==============================="
        width = -1
        for row in squares:
            for square in row:
                width = max([square.numberOfPossibilities(), width])
        line = '+'.join(['-'*width*3]*3)
        for row in range(0,9):
            print ''.join(squares[row][col].getPossibilitiesString().center(width)+('|' if col in [2,5] else '') for col in range(0,9))
            if row in [2,5]: print line
        print "==============================="
                
    def __init__(self):
        for x in range(0,9):
            self.Squares.append([])
            for y in range(0,9):
                self.Squares[x].append(Square())

def flattenArray(list):
    newList = []
    for row in range(0,len(list)):
        for col in range(0,len(list[row])):
            newList.append(list[row][col])
    return newList

GridNum = 30
grid = Grid()
row = 0
col = 0
with open("p096_sudoku.txt") as f:
    start = (GridNum-1) * 9 + GridNum
    end = start + 9
    for line in f.readlines()[start:end]:
        for num in line:
            if(num.isdigit()):
                grid.Squares[row][col].assignVal(int(num))
                grid.Squares[row][col].setCoord(row, col)
                print "setting coord", row, col
            col += 1
        row += 1
        col = 0
print "=========== Before ==========="
grid.display()
grid.smartElimination()
print "=========== After ==========="
grid.display()

Grid.Solve(grid).display()

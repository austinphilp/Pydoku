import sys
from copy import copy

class Square:
    possibilities = []

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
    def isValid(self):
        return self.numberOfPossibilities() > 0

    def eliminatePossibility(self, num):
        self.possibilities[num-1] = None
        return self.isSolved()

    def getPossibilitiesString(self):
        return ''.join(str(num) for num in self.activePossibilities())

    def setCoord(self, x, y): 
        self.x = x
        self.y = y

    def __init__(self):
        self.possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]

class Grid:
    Squares = []

    @staticmethod
    def GetCorrectSquares(squares):
        
    def smartElimination(self):
        for row in range(0,9):
            for col in range(0,9):
                if self.Squares[row][col].isSolved():
                    Grid.RemovePossibilityForRow( self.Squares, row, self.Squares[row][col].getValue() )
                    Grid.RemovePossibilityForCol( self.Squares, col, self.Squares[row][col].getValue() )
                    Grid.RemovePossibilityForSubGrid( self.Squares, row, col, self.Squares[row][col].getValue() )

    @staticmethod
    def SquaresAreValid(squares):
        for square in squares[row]:
            if not square.isSolved():
                if square.eliminatePossibility(val):
                    Grid.RemovePossibilityForRow(row, square.getValue())
    @staticmethod
    def RemovePossibilityForRow(squares, row, val):
        for square in squares[row]:
            if not square.isSolved():
                if square.eliminatePossibility(val):
                    Grid.RemovePossibilityForRow(row, square.getValue())

    @staticmethod
    def RemovePossibilityForCol(squares, col, val):
        for row in squares:
            if not row[col].isSolved():
                if row[col].eliminatePossibility(val):
                    Grid.RemovePossibilityForCol(squares, col, row[col].getValue())

    @staticmethod
    def RemovePossibilityForSubGrid(squares, squareRow, squareCol, val):
        for row in range((squareRow/3)*3, ((squareRow/3)*3)+3):
            for col in range((squareCol/3)*3, ((squareCol/3)*3)+3):
                square = squares[row][col]
                if not squares[row][col].isSolved():
                    if squares[row][col].eliminatePossibility(val):
                        Grid.RemovePossibilityForCol(col, self.Squares[row][col].getValue())

    def bruteForce(self): 
        squares = copy.copy(self.Squares)
        Grid.GetCorrectSquares(squares)


    def display(self):
        width = -1
        for row in self.Squares:
            for square in row:
                width = max([square.numberOfPossibilities(), width])
        line = '+'.join(['-'*width*3]*3)
        for row in range(0,9):
            print ''.join(self.Squares[row][col].getPossibilitiesString().center(width)+('|' if col in [2,5] else '') for col in range(0,9))
            if row in [2,5]: print line
                
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
            

GridNum = 0
grid = Grid()
row = 0
col = 0
with open("p096_sudoku.txt") as f:
    for line in f.readlines()[((GridNum*9)+1 ):GridNum+8]:
        for num in line:
            if(num.isdigit()):
                grid.Squares[row][col].assignVal(int(num))
                grid.Squares[row][col].setCoord(row, col)
            col += 1
        row += 1
        col = 0
print "=========== Before ==========="
grid.display()
grid.smartElimination()
print "=========== After ==========="
grid.display()

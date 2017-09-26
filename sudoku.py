import sys
from copy import deepcopy
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

class Grid:
    Squares = []
    
    @staticmethod
    def GetCorrectSquares(squares):
        if all(square.isSolved() for square in flattenArray(squares)):
            return deepcopy(squares)
        if not Grid.SquaresAreValid(squares):
            return None
        Grid.Display(squares)
        minVal = 9
        minSquare = None
        for row in range(0,9):
            for col in range(0,9):
                if not squares[row][col].isSolved():
                    if squares[row][col].numberOfPossibilities() < minVal:
                        minSquare = squares[row][col]
                        minVal = squares[row][col].numberOfPossibilities()

        square = minSquare
                
        #square = min([(min(row, key=getPossibilitiesValue), row) for row in squares], key=getPossibilitiesValue)
        row, col = square.x, square.y
        print row
        print col
        for possibility in square.activePossibilities():
            #raw_input("Press Enter to continue...")
            squaresBackup = deepcopy(squares)
            print "Try Possibility",possibility
            print "For Coord (",row,col,")"
            print square.isSolved()
            print squares[row][col].isSolved()
            print squares[row][col].numberOfPossibilities()
            Grid.Display(squares)
            squares[row][col].assignVal(possibility)
            Grid.RemovePossibilityForRow( squares, squares[row][col] )
            Grid.RemovePossibilityForCol( squares, squares[row][col] )
            Grid.RemovePossibilityForSubGrid( squares, squares[row][col] )
            if Grid.GetCorrectSquares(deepcopy(squares)) != None:
                return squares
            else:
                squares = squaresBackup
        return None

    def smartElimination(self):
        for row in range(0,9):
            for col in range(0,9):
                if self.Squares[row][col].isSolved():
                    Grid.RemovePossibilityForRow( self.Squares, self.Squares[row][col] )
                    Grid.RemovePossibilityForCol( self.Squares, self.Squares[row][col] )
                    Grid.RemovePossibilityForSubGrid( self.Squares, self.Squares[row][col] )

    @staticmethod
    def SquaresAreValid(squares):
        for row in squares:
            for square in row:
                if not square.isValid():
                    return False
        return True
    @staticmethod
    #def RemovePossibilityForRow(squares, row, val):
    def RemovePossibilityForRow(squares, square):
        row = square.x
        print "row", row, "for", square.getValue(), "from col ", square.y

        #Grid.Display(squares)
        for col in range(0,9):
            if not col == square.y:
                if squares[row][col].eliminatePossibility(square.getValue()):
                    if not squares[row][col].isValid(): 
                        print "FOUND INVALID"
                        return
                    #print "SOLVED", square.y, ",", row, "with val", square.getValue()
                    Grid.RemovePossibilityForSubGrid(squares, squares[row][col])
                    Grid.RemovePossibilityForRow(squares, squares[row][col])
                    Grid.RemovePossibilityForCol(squares, squares[row][col])
        return squares

    @staticmethod
    #def RemovePossibilityForCol(squares, col, val):
    def RemovePossibilityForCol(squares, square):
        col = square.y
        print "col", col, "for", square.getValue(), "from row ", square.x 
        #Grid.Display(squares)
        for row in range(0,9):
            if not squares[row][col].x == square.x:
                if squares[row][col].eliminatePossibility(square.getValue()):
                    if not squares[row][col].isValid(): 
                        print "FOUND INVALID"
                        return
                    #print "SOLVED", col, ",", row[col].x, "with val", row[col].getValue()
                    Grid.RemovePossibilityForSubGrid(squares, squares[row][col])
                    Grid.RemovePossibilityForRow(squares, squares[row][col])
                    Grid.RemovePossibilityForCol(squares, squares[row][col])


    @staticmethod
    #def RemovePossibilityForSubGrid(squares, squareRow, squareCol, val):
    def RemovePossibilityForSubGrid(squares, square):
        print "grid", square.x, square.y, "for", square.getValue()
        Grid.Display(squares)
        
        if square.getValue() == None:
            return
        for row in range((square.x/3)*3, ((square.x/3)*3)+3):
            for col in range((square.y/3)*3, ((square.y/3)*3)+3):
                if row != square.x and col != square.y:
                    print row, col, square.x, square.y
                    if squares[row][col].eliminatePossibility(square.getValue()):
                        if not squares[row][col].isValid(): 
                            print "FOUND INVALID"
                            return
                        #print "SOLVED", col, ",", row, "with val", squares[row][col].getValue()
                        Grid.RemovePossibilityForSubGrid(squares, squares[row][col])
                        Grid.RemovePossibilityForRow(squares, squares[row][col])
                        Grid.RemovePossibilityForCol(squares, squares[row][col])

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

def getPossibilitiesValue(s):
    if s.isSolved():
        return 9
    else:
        return s.numberOfPossibilities()
            
sys.setrecursionlimit(10000)
GridNum = 4
grid = Grid()
row = 0
col = 0
with open("p096_sudoku.txt") as f:
    for line in f.readlines()[((GridNum*9)+GridNum+1):(GridNum*9)+GridNum+1+8]:
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

#grid.bruteForce()

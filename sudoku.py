import sys
from copy import deepcopy

PUZZLE_FILE = "p096_sudoku.txt"

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

    def isValid(self):
        return self.numberOfPossibilities() > 0

    def eliminatePossibility(self, num):
        if num == None: return False
        previouslySolved = self.isSolved()
        self.possibilities[num-1] = None
        return self.isSolved() and not previouslySolved

    def getPossibilitiesString(self):
        return ''.join(str(num) for num in self.activePossibilities())

    def __init__(self, x, y, val):
        self.possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.x = x
        self.y = y
        self.assignVal(val)

class Grid:
    Squares = []
    
    @staticmethod
    def Solve(grid):
        # if the grid is solved, 
        if grid.isSolved():
            return grid
        # if the grid is now invalid, return None
        if not grid.isValid():
            return None

        # Get the square with the least amount of possible values
        square = grid.getMostSolvedSquare()
        row, col = square.x, square.y

        # try each possible value 
        for possibility in square.activePossibilities():
            #Backup a copy of the squares to restore if branch fails
            backupSquares = deepcopy(grid.Squares)

            #Assign the possible value and perform a smart elimination
            grid.Squares[row][col].assignVal(possibility)
            grid.smartElimination()

            #Attempt to solve the new grid
            result = Grid.Solve(grid)
            
            # result will only be None if the grid was not valid
            if result is not None:
                return result
            else:
                grid.Squares  = backupSquares
        return None

    # Return True if all squares have only one possible value
    def isSolved(self):
        return all(square.isSolved() for square in flattenArray(deepcopy(self.Squares)))

    # Return the square that has the least possible values
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

    # Eliminate possibilities for squares based on the known values of other squares following the rules of sudoku
    def smartElimination(self):
        solved = [square for square in flattenArray(self.Squares) if square.isSolved()]
        while len(solved) > 0:
            square = solved.pop(0)
            solved += self.RemovePossibilityForRow( square )
            solved += self.RemovePossibilityForCol( square )
            solved += self.RemovePossibilityForSubGrid( square )

    # Return true if every square in the grid has at least 1 value
    def isValid(self):
        return all(square.isValid() for square in flattenArray(deepcopy(self.Squares)))

    # Remove the value of the given square from the possibilities of every other square in its row
    def RemovePossibilityForRow(self, square):
        solved = []
        row = square.x
        for col in range(0,9):
            if not col == square.y:
                if self.Squares[row][col].eliminatePossibility(self.Squares[square.x][square.y].getValue()):
                    if not self.Squares[row][col].isValid(): 
                        print "FOUND INVALID"
                        return None
                    else:
                        solved.append(deepcopy(self.Squares[row][col]))
        return solved

    # Remove the value of the given square from the possibilities of every other square in its column
    def RemovePossibilityForCol(self, square):
        solved = []
        col = square.y
        for row in range(0,9):
            if not self.Squares[row][col].x == square.x:
                if self.Squares[row][col].eliminatePossibility(self.Squares[square.x][square.y].getValue()):
                    if not self.Squares[row][col].isValid(): 
                        print "FOUND INVALID"
                        return None
                    else:
                        solved.append(deepcopy(self.Squares[row][col]))
        return solved

    # Remove the value of the given square from the possibilities of every other square in its subgrid
    def RemovePossibilityForSubGrid(self, square):
        solved = []
        if square.getValue() == None:
            return 
        for row in range((square.x/3)*3, ((square.x/3)*3)+3):
            for col in range((square.y/3)*3, ((square.y/3)*3)+3):
                if row != square.x and col != square.y:
                    if self.Squares[row][col].eliminatePossibility(self.Squares[square.x][square.y].getValue()):
                        if not self.Squares[row][col].isValid(): 
                            print "FOUND INVALID"
                            return None
                        else:
                            solved.append(deepcopy(self.Squares[row][col]))
        return solved

    # Print the grid out, displaying every possible value for that square
    def display(self):
        line = '+'.join(['-'*3]*3)
        for row in range(0,9):
            print ''.join(str(self.Squares[row][col].getValue() or "*")+('|' if col in [2,5] else '') for col in range(0,9))
            if row in [2,5]: print line
                
    # construct the grid from a given array of lines from the sudoku file
    def __init__(self, lines):
        for line in lines:
            self.Squares.append([])
            for num in [x for x in line if x.isdigit()]:
                row = len(self.Squares)-1
                col = len(self.Squares[row])
                self.Squares[row].append(Square(row,col,int(num)))

# convert a 2d array into a 1d array
def flattenArray(list):
    newList = []
    for row in range(0,len(list)):
        for col in range(0,len(list[row])):
            newList.append(list[row][col])
    return newList

if len(sys.argv) < 2:
    print "ERR: No puzzle number provided"
    print "Example Usage : $ python pydoku.py <PUZZLE_NUMBER>"
    exit()
else: 
    try:
        GridNum = int(sys.argv[1])
    except ValueError:
        print "Argument provided is invalid, defaulting to 1"
start = (GridNum-1)*9+GridNum
end = start + 9
with open(PUZZLE_FILE) as f:
    grid = Grid(f.readlines()[start:end])
print "=========== Puzzle ==========="
grid.display()
raw_input("Press Enter to reveal solution")
print "\n=========== Solution ==========="
grid.smartElimination()
Grid.Solve(grid).display()

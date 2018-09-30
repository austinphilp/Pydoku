import constants
from copy import deepcopy
from square import Square


class Grid(object):
    Squares = []

    # construct the grid from a given array of lines from the sudoku file
    def __init__(self, lines):
        for line in lines:
            self.Squares.append([])
            for num in [x for x in line if x.isdigit()]:
                row = len(self.Squares)-1
                col = len(self.Squares[row])
                self.Squares[row].append(Square(row, col, int(num)))

    def bruteForce(self):
        # if the grid is solved
        if self.isSolved():
            return self

        # if the grid is now invalid, return None
        if not self.isValid():
            return None

        # Get the square with the least amount of possible values
        row, col = self.getMostSolvedSquare().getCoord()

        # try each possible value
        for possibility in self.Squares[row][col].activePossibilities():
            # Backup a copy of the squares to restore if branch fails
            backupSquares = deepcopy(self.Squares)

            # Assign the possible value
            self.Squares[row][col].assignVal(possibility)

            # Attempt to solve the new grid
            result = self.solve()

            # result will only be None if the grid was not valid
            if result is not None:
                return result
            else:
                self.Squares = backupSquares

        return None

    # Return True if all squares have only one possible value
    def isSolved(self):
        for row in range(0, constants.SUDOKU_GRID_SIZE):
            for col in range(0, constants.SUDOKU_GRID_SIZE):
                if not self.Squares[row][col].isSolved():
                    return False
        return True

    # Return the square that has the least possible values
    def getMostSolvedSquare(self):
        minVal = 9
        minSquare = None
        for row in range(0, constants.SUDOKU_GRID_SIZE):
            for col in range(0, constants.SUDOKU_GRID_SIZE):
                if not self.Squares[row][col].isSolved():
                    if self.Squares[row][col].numberOfPossibilities() < minVal:
                        minSquare = self.Squares[row][col]
                        minVal = self.Squares[row][col].numberOfPossibilities()
        return minSquare

    # Return a list of all squares in the grid that are solved
    def getSolvedSquares(self):
        solved = []
        for row in range(0, constants.SUDOKU_GRID_SIZE):
            for col in range(0, constants.SUDOKU_GRID_SIZE):
                if self.Squares[row][col].isSolved():
                    solved.append(self.Squares[row][col])
        return solved

    # Eliminate possibilities for squares based on the known
    # values of other squares following the rules of sudoku
    def smartElimination(self):
        solved = self.getSolvedSquares()
        while len(solved) > 0:
            square = solved.pop(0)
            solved += self.removePossibilityForRow(square)
            solved += self.removePossibilityForCol(square)
            solved += self.removePossibilityForSubGrid(square)

    # Return true if every square in the grid has at least 1 value
    def isValid(self):
        for row in range(0, constants.SUDOKU_GRID_SIZE):
            for col in range(0, constants.SUDOKU_GRID_SIZE):
                if not self.Squares[row][col].isValid():
                    return False
        return True

    # Remove the value of the given square from the
    # possibilities of every other square in its row
    def removePossibilityForRow(self, square):
        solved = []
        row = square.x
        for col in range(0, constants.SUDOKU_GRID_SIZE):
            # Only perform the elimination if the square in
            # question is not the one passed into this function
            if not col == square.y:
                # if eliminating that possibility solved
                # the square, add it to the solved list
                if self.Squares[row][col].eliminatePossibility(
                        square.getValue()):
                    solved.append(self.Squares[row][col])
        return solved

    # Remove the value of the given square from the
    # possibilities of every other square in its column
    def removePossibilityForCol(self, square):
        solved = []
        col = square.y
        for row in range(0, constants.SUDOKU_GRID_SIZE):
            # Only perform the elimination if the square in question
            # is not the one passed into this function
            if not self.Squares[row][col].x == square.x:
                # if eliminating that possibility solved
                # the square, add it to the solved list
                if self.Squares[row][col].eliminatePossibility(
                        square.getValue()):
                    solved.append(self.Squares[row][col])
        return solved

    # Remove the value of the given square from the
    # possibilities of every other square in its subgrid
    def removePossibilityForSubGrid(self, square):
        solved = []
        if square.getValue() is None:
            return None
        for row in range((square.x//3)*3, ((square.x//3)*3)+3):
            for col in range((square.y//3)*3, ((square.y//3)*3)+3):
                # Only perform the elimination if the square in
                # question is not the one passed into this function
                if row != square.x and col != square.y:
                    # if eliminating that possibility solved
                    # the square, add it to the solved list
                    if self.Squares[row][col].eliminatePossibility(
                            square.getValue()):
                        solved.append(self.Squares[row][col])
        return solved

    # Print the grid out, displaying every possible value for that square
    def display(self):
        line = '+'.join(['-'*3]*3)
        for row in range(0, constants.SUDOKU_GRID_SIZE):
            print(
                ''.join(
                    str(self.Squares[row][col].getValue() or "*") +
                    ('|' if col in [2, 5] else '')
                    for col in range(0, constants.SUDOKU_GRID_SIZE)
                )
            )
            if row in [2, 5]:
                print(line)

    # First use intelligent methods to eliminate as many methods as possible,
    def solve(self):
        self.smartElimination()
        return self.bruteForce()

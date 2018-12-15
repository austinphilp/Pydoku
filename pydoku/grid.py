from constants import SUDOKU_GRID_SIZE
from copy import deepcopy
from square import Square


class Grid(object):

    # construct the grid from a given array of lines from the sudoku file
    def __init__(self, lines):
        self.squares = []
        for line in lines:
            self.squares.append([])
            for num in [int(x) for x in line if x.isdigit()]:
                row = len(self.squares)-1
                col = len(self.squares[row])
                self.squares[row].append(Square(row, col, num))

    def brute_force(self):
        if self.is_solved:
            return self

        # if the grid is now invalid, return None
        if not self.is_valid:
            return None

        # Get the square with the least amount of possible values
        row, col = self.get_most_solved_square().coord

        # try each possible value
        for possibility in self.squares[row][col].possibilities:
            # Backup a copy of the squares to restore if branch fails
            backup_squares = deepcopy(self.squares)

            # Assign the possible value
            self.squares[row][col].value = possibility

            # Attempt to solve the new grid
            result = self.solve()

            # result will only be None if the grid was not valid
            if result is not None:
                return result
            else:
                self.squares = backup_squares
                self.squares[row][col].possibilities.discard(possibility)

        return None

    # Return True if all squares have only one possible value
    @property
    def is_solved(self):
        return self.check_filled_in() and \
            self.check_rows_unique() and \
            self.check_col_unique()

    def check_filled_in(self):
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if not self.squares[row][col].is_solved:
                    return False
        return True

    def check_rows_unique(self):
        for row in range(0, SUDOKU_GRID_SIZE):
            row_vals = [
                self.squares[row][col].value
                for col in range(0, SUDOKU_GRID_SIZE)
                if self.squares[row][col].is_solved
            ]
            if len(row_vals) != len(set(row_vals)):
                return False
        return True

    def check_col_unique(self):
        for col in range(0, SUDOKU_GRID_SIZE):
            col_values = [
                self.squares[row][col].value
                for row in range(0, SUDOKU_GRID_SIZE)
                if self.squares[row][col].is_solved
            ]
            if len(col_values) != len(set(col_values)):
                return False
        return True

    # Return the square that has the least possible values
    def get_most_solved_square(self):
        min_val = 10
        min_square = None
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if not self.squares[row][col].is_solved:
                    if len(self.squares[row][col].possibilities) < min_val:
                        min_square = self.squares[row][col]
                        min_val = len(self.squares[row][col].possibilities)
        return min_square

    # Return a list of all squares in the grid that are solved
    def get_solved_squares(self):
        solved = []
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if self.squares[row][col].is_solved:
                    solved.append(self.squares[row][col])
        return solved

    # Eliminate possibilities for squares based on the known
    # values of other squares following the rules of sudoku
    def smart_elimination(self):
        solved = self.get_solved_squares()
        while len(solved) > 0:
            square = solved.pop(0)
            solved += self.remove_possibility_for_row(square)
            solved += self.remove_possibility_for_col(square)
            solved += self.remove_possibility_for_subgrid(square)

    # Return true if every square in the grid has at least 1 value
    @property
    def is_valid(self):
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if not self.squares[row][col].is_valid:
                    return False
        return self.check_rows_unique() and self.check_col_unique()

    # Remove the value of the given square from the
    # possibilities of every other square in its row
    def remove_possibility_for_row(self, square):
        solved = []
        row = square.x
        for col in range(0, SUDOKU_GRID_SIZE):
            # Only perform the elimination if the square in
            # question is not the one passed into this function
            if (row, col) != (square.x, square.y):
                # if eliminating that possibility solved
                # the square, add it to the solved list
                if self.squares[row][col].remove_possibility(square.value):
                    solved.append(self.squares[row][col])
        return solved

    # Remove the value of the given square from the
    # possibilities of every other square in its column
    def remove_possibility_for_col(self, square):
        solved = []
        col = square.y
        for row in range(0, SUDOKU_GRID_SIZE):
            # Only perform the elimination if the square in question
            # is not the one passed into this function
            if not self.squares[row][col].x == square.x:
                # if eliminating that possibility solved
                # the square, add it to the solved list
                if self.squares[row][col].remove_possibility(square.value):
                    solved.append(self.squares[row][col])
        return solved

    # Remove the value of the given square from the
    # possibilities of every other square in its subgrid
    def remove_possibility_for_subgrid(self, square):
        solved = []
        for row in range((square.x//3)*3, ((square.x//3)*3)+3):
            for col in range((square.y//3)*3, ((square.y//3)*3)+3):
                # Only perform the elimination if the square in
                # question is not the one passed into this function
                if row != square.x and col != square.y:
                    # if eliminating that possibility solved
                    # the square, add it to the solved list
                    if self.squares[row][col].remove_possibility(square.value):
                        solved.append(self.squares[row][col])
        return solved

    # Print the grid out, displaying every possible value for that square
    def display(self):
        line = '+'.join(['-'*3]*3)
        for row in range(0, SUDOKU_GRID_SIZE):
            print(
                ''.join(
                    str(self.squares[row][col].value or "*") +
                    ('|' if col in [2, 5] else '')
                    for col in range(0, SUDOKU_GRID_SIZE)
                )
            )
            if row in [2, 5]:
                print(line)

    # First use intelligent methods to eliminate as many methods as possible,
    def solve(self):
        self.smart_elimination()
        return self.brute_force()

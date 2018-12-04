from constants import SUDOKU_GRID_SIZE
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

    def brute_force(self):
        # TODO(Austin) The alg seems to be running in a loop

        print()
        self.display()
        if self.is_solved:
            return self

        # if the grid is now invalid, return None
        if not self.is_valid():
            return None

        # Get the square with the least amount of possible values
        row, col = self.get_most_solved_square().get_coord()

        # try each possible value
        for possibility in self.Squares[row][col].possibilities:
            # Backup a copy of the squares to restore if branch fails
            backup_squares = deepcopy(self.Squares)

            # Assign the possible value
            self.Squares[row][col].assign_val(possibility)

            # Attempt to solve the new grid
            result = self.solve()

            # result will only be None if the grid was not valid
            if result is not None:
                return result
            else:
                self.Squares = backup_squares
                self.Squares[row][col].possibilities.discard(possibility)

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
                if not self.Squares[row][col].is_solved:
                    return False
        return True

    def check_rows_unique(self):
        for row in range(0, SUDOKU_GRID_SIZE):
            row_vals = [
                self.Squares[row][col].value
                for col in range(0, SUDOKU_GRID_SIZE)
                if self.Squares[row][col].is_solved
            ]
            if len(row_vals) != len(set(row_vals)):
                return False
        return True

    def check_col_unique(self):
        i = 0
        for col in range(0, SUDOKU_GRID_SIZE):
            col_values = [
                self.Squares[row][col].value
                for row in range(0, SUDOKU_GRID_SIZE)
                if self.Squares[row][col].is_solved
            ]
            if len(col_values) != len(set(col_values)):
                # print(F"Failing Col - {i}")
                # print(F"Col Values - {''.join(str(v) for v in col_values)}")
                # print(F"List - {len(col_values)}")
                # print(F"Set - {len(set(col_values))}")
                return False
            i += 1
        return True

    # Return the square that has the least possible values
    def get_most_solved_square(self):
        min_val = 10
        min_square = None
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if not self.Squares[row][col].is_solved:
                    if len(self.Squares[row][col].possibilities) < min_val:
                        min_square = self.Squares[row][col]
                        min_val = len(self.Squares[row][col].possibilities)
        return min_square

    # Return a list of all squares in the grid that are solved
    def get_solved_squares(self):
        solved = []
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if self.Squares[row][col].is_solved:
                    solved.append(self.Squares[row][col])
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
    def is_valid(self):
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if not self.Squares[row][col].is_valid():
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
            if not col == square.y:
                # if eliminating that possibility solved
                # the square, add it to the solved list
                if self.Squares[row][col].eliminate_possibility(
                        square.value):
                    solved.append(self.Squares[row][col])
        return solved

    # Remove the value of the given square from the
    # possibilities of every other square in its column
    def remove_possibility_for_col(self, square):
        solved = []
        col = square.y
        for row in range(0, SUDOKU_GRID_SIZE):
            # Only perform the elimination if the square in question
            # is not the one passed into this function
            if not self.Squares[row][col].x == square.x:
                # if eliminating that possibility solved
                # the square, add it to the solved list
                if self.Squares[row][col].eliminate_possibility(
                        square.value):
                    solved.append(self.Squares[row][col])
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
                    if self.Squares[row][col].eliminate_possibility(square.value):
                        solved.append(self.Squares[row][col])
        return solved

    # Print the grid out, displaying every possible value for that square
    def display(self):
        line = '+'.join(['-'*3]*3)
        for row in range(0, SUDOKU_GRID_SIZE):
            print(
                ''.join(
                    str(self.Squares[row][col].value or "*") +
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

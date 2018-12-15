from constants import SUDOKU_GRID_SIZE
from copy import deepcopy


class Solver(object):

    # construct the grid from a given array of lines from the sudoku file
    def __init__(self, grid):
        self.grid = grid

    def brute_force(self):
        if self.is_solved:
            return True

        # if the grid is now invalid, return None
        if not self.is_valid:
            return False

        # Get the square with the least amount of possible values
        row, col = self.get_most_solved_square().coord

        # try each possible value
        for possibility in self.grid[row][col].possibilities:
            # Create a solver instance for the new grid possibility
            solver = Solver(deepcopy(self.grid))
            solver.grid[row][col].value = possibility

            # Attempt to solve the new grid, use it if it is solved
            if solver.solve() is True:
                self.grid = solver.grid
                return True
        return False

    # Return True if all squares have only one possible value
    @property
    def is_solved(self):
        return self.check_filled_in() and \
            self.check_rows_unique() and \
            self.check_col_unique()

    def check_filled_in(self):
        return all(square.is_solved for square in self.grid)

    def check_rows_unique(self):
        for row in range(0, SUDOKU_GRID_SIZE):
            row_vals = [
                self.grid[row][col].value
                for col in range(0, SUDOKU_GRID_SIZE)
                if self.grid[row][col].is_solved
            ]
            if len(row_vals) != len(set(row_vals)):
                return False
        return True

    def check_col_unique(self):
        for col in range(0, SUDOKU_GRID_SIZE):
            col_values = [
                self.grid[row][col].value
                for row in range(0, SUDOKU_GRID_SIZE)
                if self.grid[row][col].is_solved
            ]
            if len(col_values) != len(set(col_values)):
                return False
        return True

    # Return the square that has the least possible values
    def get_most_solved_square(self):
        return min(
            [square for square in self.grid if not square.is_solved],
            key=lambda s: len(s.possibilities)
        )

    # Return a list of all squares in the grid that are solved
    def get_solved_squares(self):
        return [square for square in self.grid if square.is_solved]

    # Eliminate possibilities for squares based on the known
    # values of other squares following the rules of sudoku
    def smart_elimination(self):
        solved = self.get_solved_squares()
        while len(solved) > 0:
            square = solved.pop(0)
            solved += self.remove_possibility_for_row(square)
            solved += self.remove_possibility_for_col(square)
            solved += self.remove_possibility_for_subgrid(square)
        return solved

    # Return true if every square in the grid has at least 1 value
    @property
    def is_valid(self):
        for row in range(0, SUDOKU_GRID_SIZE):
            for col in range(0, SUDOKU_GRID_SIZE):
                if not self.grid[row][col].is_valid:
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
                if self.grid[row][col].remove_possibility(square.value):
                    solved.append(self.grid[row][col])
        return solved

    # Remove the value of the given square from the
    # possibilities of every other square in its column
    def remove_possibility_for_col(self, square):
        solved = []
        col = square.y
        for row in range(0, SUDOKU_GRID_SIZE):
            # Only perform the elimination if the square in question
            # is not the one passed into this function
            if not self.grid[row][col].x == square.x:
                # if eliminating that possibility solved
                # the square, add it to the solved list
                if self.grid[row][col].remove_possibility(square.value):
                    solved.append(self.grid[row][col])
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
                    if self.grid[row][col].remove_possibility(square.value):
                        solved.append(self.grid[row][col])
        return solved

    # First use intelligent methods to eliminate as many methods as possible,
    def solve(self):
        self.smart_elimination()
        self.brute_force()
        return self.is_solved and self.is_valid

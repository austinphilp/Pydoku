from copy import deepcopy


class Solver(object):

    # construct the grid from a given array of lines from the sudoku file
    def __init__(self, grid):
        self.grid = grid

    def brute_force(self):
        if self.is_solved:
            return True
        elif not self.is_valid:
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

    @property
    def is_valid(self):
        """
        Return true if every square in the grid has at least 1 value
        """
        return all(s.is_valid for s in self.grid) and \
            all(row.is_valid for row in self.grid.rows) and \
            all(col.is_valid for col in self.grid.cols)

    # Return True if all squares have only one possible value
    @property
    def is_solved(self):
        return all(square.is_solved for square in self.grid) and self.is_valid

    # Return the square that has the least possible values
    def get_most_solved_square(self):
        return min(
            [square for square in self.grid if not square.is_solved],
            key=lambda s: len(s.possibilities)
        )

    # Return a list of all squares in the grid that are solved
    def get_solved_squares(self):
        return [square for square in self.grid if square.is_solved]

    def smart_elimination(self):
        """
        Eliminate possibilities for squares based on the known
        values of other squares following the rules of sudoku
        """
        solved = self.get_solved_squares()
        while len(solved) > 0:
            square = solved.pop(0)
            solved += self.remove_possibility_for_collection(
                collection=(
                    self.grid.get_row(square.x) +
                    self.grid.get_col(square.y)
                ),
                value=square.value
            )
            solved += self.remove_possibility_for_subgrid(square)
        return solved

    def remove_possibility_for_collection(self, collection, value):
        """
        Remove a value from the possible values for a squares in a collection.

        Return the squares that were solved by this change
        """
        return [
            square for square in collection
            if not square.is_solved and square.remove_possibility(value)
        ]

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

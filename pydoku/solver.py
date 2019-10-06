from copy import deepcopy


class Solver(object):
    def __init__(self, grid):
        self.grid = grid

    @property
    def is_solved(self):
        """
        Returns:
            bool - True if every square in the grid has a solution and the grid
            is considered valid
        """
        return all(square.is_solved for square in self.grid) and \
            self.grid.is_valid

    def brute_force(self):
        """
        A DFS on the decision tree of the remaining possible values for every
        unsolved square on the grid, attempting to find by force a solution to
        the puzzle grid

        Returns:
            None
        """

        # Get the square with the least amount of possible values
        square = self.get_most_solved_square()
        for possibility in square.possibilities:
            # Create a solver instance for the new grid possibility
            solver = self.copy()
            solver.grid[square.x][square.y].value = possibility

            # Attempt to solve the new grid, use it if it is solved
            if solver.grid.is_valid and solver.solve() is True:
                self.grid = solver.grid
                return

    def copy(self):
        """
        Create a deep copy of the puzzle solver and its grid

        Returns:
            Solver - A deep copy of this solver and its grid
        """
        return Solver(deepcopy(self.grid))

    def get_most_solved_square(self):
        """
        Returns:
            Square - The square that has the lowest amount of possible values
        """
        return min(
            [square for square in self.grid if not square.is_solved],
            key=lambda s: len(s.possibilities)
        )

    def get_solved_squares(self):
        """
        Returns:
            list - All squares in the grid that are solved
        """
        return [square for square in self.grid if square.is_solved]

    def remove_possibility_for_collection(self, collection, value):
        """
        Remove a value from the possible values for a squares in a collection.

        Returns:
            list - The squares that were solved by this change
        """
        return [
            square for square in collection
            if not square.is_solved and square.remove_possibility(value)
        ]

    def smart_elimination(self):
        """
        Attempt to solve the puzzle by using the values of solved squares to
        eliminate possibilities in unsolved squares adjacent to them

        Returns:
            list - The squares that were solved by this step
        """
        solved = self.get_solved_squares()
        while len(solved) > 0:
            square = solved.pop(0)
            solved += self.remove_possibility_for_collection(
                collection=self.grid.get_intersection_for_square(square),
                value=square.value
            )
        return solved

    def solve(self):
        """
        Attempt to solve the puzzle, first using smart elimination methods, and
        then (assuming a solution could not be found) by the use of a brute
        force DFS on the puzzle's decision tree

        Returns:
            bool - flag representing whether or not the puzzle was solved
        """
        self.smart_elimination()
        if not self.is_solved:
            self.brute_force()
        return self.is_solved and self.grid.is_valid

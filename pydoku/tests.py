from solver import Solver
from utils import load_grid_from_file


def _test_puzzle(grid_num):
    """
    This method will be used to dynamically generate puzzle tests using the
    preloaded puzzles (within the puzzles/ folder at project root)

    Arguments:
        grid_num(int) - The id of the grid you would like to test within the
        p096_sudoku.txt test folder

    Asserts:
        After running the loaded puzzle through the Solver.solve method, assert
        that the puzzle is solved (All squares have exactly 1 possible value)
    """
    grid = load_grid_from_file(grid_num)
    solver = Solver(grid)
    solver.solve()
    assert solver.is_solved


# Auto generate puzzle tests to test each puzzle in the puzzle file
# independently, without having to write 50 different test cases
for n in range(0, 50):
    locals()[F"test_puzzle_{n}"] = lambda: _test_puzzle(n)

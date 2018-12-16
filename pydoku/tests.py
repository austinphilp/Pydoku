from solver import Solver
from utils import load_grid_from_file


def _test_puzzle(grid_num):
    grid = load_grid_from_file(grid_num)
    solver = Solver(grid)
    solver.solve()
    assert solver.is_solved


for n in range(0, 50):
    locals()[F"test_puzzle_{n}"] = lambda: _test_puzzle(n)

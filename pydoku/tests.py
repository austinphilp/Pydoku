from utils import load_grid_from_file


def _test_puzzle(grid_num):
    grid = load_grid_from_file(grid_num)
    grid.solve()
    assert grid.is_solved


for n in range(1, 50):
    locals()[F"test_puzzle_{n}"] = lambda: _test_puzzle(n)

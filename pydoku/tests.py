from utils import load_grid_from_file


def _test_puzzle(grid_num):
    grid = load_grid_from_file(grid_num)
    grid.solve()
    return grid.is_solved


def test_all_puzzles_work():
    for grid_num in range(1, 50):
        assert _test_puzzle(grid_num)

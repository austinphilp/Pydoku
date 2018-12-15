import constants
from grid import Grid


def load_grid_from_file(grid_num):
    puzzle_exists = (
        grid_num <= constants.MAX_PUZZLE_NUM and
        grid_num >= constants.MIN_PUZZLE_NUM
    )
    assert puzzle_exists
    with open(constants.PUZZLE_FILE) as f:
        return Grid.load_from_file(f.readlines()[(grid_num*10)-9:grid_num*10])

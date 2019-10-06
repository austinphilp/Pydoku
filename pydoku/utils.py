import os

import constants
from grid import Grid


def load_grid_from_file(grid_num):
    puzzle_exists = (
        grid_num <= constants.MAX_PUZZLE_NUM and
        grid_num >= constants.MIN_PUZZLE_NUM
    )
    assert puzzle_exists
    # Get file path relative to this module
    file_path = os.path.join(os.path.dirname(__file__), constants.PUZZLE_FILE)
    with open(file_path) as f:
        return Grid.load_from_file(f.readlines()[(grid_num*10)-9:grid_num*10])

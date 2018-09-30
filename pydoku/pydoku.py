import sys

import constants
from grid import Grid


def main(grid_num):
    if len(sys.argv) < 2:
        print("ERR: No puzzle number provided")
        print("Example Usage : $ python pydoku.py <PUZZLE_NUMBER>")
        exit()
    else:
        with open(constants.PUZZLE_FILE) as f:
            grid = Grid(f.readlines()[(grid_num*10)-9:grid_num*10])

        print("=========== Unsolved Puzzle ===========")
        grid.display()
        input("Press Enter to reveal solution")
        print("\n=========== Solution ===========")
        grid.solve().display()

if __name__ == "__main__":
    grid_num = int(sys.argv[1])
    puzzle_exists = (
        grid_num <= constants.MAX_PUZZLE_NUM and
        grid_num >= constants.MIN_PUZZLE_NUM
    )
    assert puzzle_exists
    main(grid_num)

import sys

import constants
from grid import Grid


if len(sys.argv) < 2:
    print("ERR: No puzzle number provided")
    print("Example Usage : $ python pydoku.py <PUZZLE_NUMBER>")
    exit()
else:
    try:
        puzzle_exists = (
            int(sys.argv[1]) <= constants.MAX_PUZZLE_NUM and
            int(sys.argv[1]) >= constants.MIN_PUZZLE_NUM
        )
        if puzzle_exists:
            GridNum = int(sys.argv[1])
            with open(constants.PUZZLE_FILE) as f:
                grid = Grid(f.readlines()[(GridNum*10)-9:GridNum*10])

            print("=========== Unsolved Puzzle ===========")
            grid.display()
            input("Press Enter to reveal solution")
            print("\n=========== Solution ===========")
            grid.solve().display()
        else:
            print(
                "Puzzle Number is out of range, "
                "please choose a puzzle from 1 - 50"
            )
    except ValueError:
        print("Argument provided is invalid, defaulting to 1")

# Read the relevant lines from the sudoku file and construct a grid with them

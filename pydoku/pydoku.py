import sys

from utils import load_grid_from_file


def main(grid_num):
    grid = load_grid_from_file(grid_num)
    print("=========== Unsolved Puzzle ===========")
    grid.display()
    input("Press Enter to reveal solution")
    print("\n=========== Solution ===========")
    grid.solve().display()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERR: No puzzle number provided")
        print("Example Usage : $ python pydoku.py <PUZZLE_NUMBER>")
        exit()
    else:
        main(grid_num=int(sys.argv[1]))

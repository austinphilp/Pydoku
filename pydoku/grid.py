from constants import SUDOKU_GRID_SIZE
from square import Square


class SquareCollection(object):
    def __init__(self, squares):
        self._squares = squares

    def __getitem__(self, key):
        return self._squares[key]

    def __iter__(self):
        return (square for square in self._squares)


class Row(SquareCollection):
    pass


class Col(SquareCollection):
    pass


class Grid(SquareCollection):
    # construct the grid from a given array of lines from the sudoku file
    @classmethod
    def load_from_file(cls, lines):
        squares = []
        for line in lines:
            squares.append([])
            for num in [int(x) for x in line if x.isdigit()]:
                row = len(squares)-1
                col = len(squares[row])
                squares[row].append(Square(row, col, num))
        return cls(squares)

    @property
    def rows(self):
        return [self.get_row(x) for x in range(0, SUDOKU_GRID_SIZE)]

    @property
    def cols(self):
        return [self.get_col(x) for x in range(0, SUDOKU_GRID_SIZE)]

    def get_row(self, num):
        return Row(self[num])

    def get_col(self, num):
        return Col([
            s for row in range(0, SUDOKU_GRID_SIZE)
            for s in self[row][num]
        ])

    # Print the grid out, displaying every possible value for that square
    def display(self):
        line = '+'.join(['-'*3]*3)
        for row in range(0, SUDOKU_GRID_SIZE):
            print(
                ''.join(
                    str(self._squares[row][col].value or "*") +
                    ('|' if col in [2, 5] else '')
                    for col in range(0, SUDOKU_GRID_SIZE)
                )
            )
            if row in [2, 5]:
                print(line)

    def __iter__(self):
        return (
            self._squares[x][y] for x in range(0, SUDOKU_GRID_SIZE)
            for y in range(0, SUDOKU_GRID_SIZE)
        )

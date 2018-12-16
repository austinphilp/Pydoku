from square import Square


class SquareCollection(object):
    def __init__(self, squares):
        self._squares = squares

    @property
    def is_valid(self):
        return all(square.is_valid for square in self) and \
            len(self) == (len(set(self)))

    def __add__(self, other):
        if isinstance(other, BaseGrid):
            return SquareCollection(self._squares + [s for s in other])
        elif isinstance(other, SquareCollection):
            return SquareCollection(self._squares + other._squares)
        else:
            raise TypeError

    def __getitem__(self, key):
        return self._squares[key]

    def __len__(self):
        return len([s for s in self._squares])

    def __repr__(self):
        formatted_str = str(self).replace('\n', '')
        return F"<{self.__class__.__name__} {formatted_str}>"

    def __str__(self):
        values = [str(square) for square in self]
        # Insert breaks to deliniate subgrid boundries
        values.insert(3, '|')
        values.insert(7, '|')
        return ''.join(values)


class BaseGrid(SquareCollection):
    def __add__(self, other):
        if isinstance(other, BaseGrid):
            return SquareCollection([s for s in self] + [s for s in other])
        elif isinstance(other, SquareCollection):
            return SquareCollection([s for s in self] + other._squares)
        else:
            raise TypeError

    def __iter__(self):
        return (
            self._squares[x][y] for x in range(0, len(self))
            for y in range(0, len(self))
        )


class Subgrid(BaseGrid):
    pass


class Grid(BaseGrid):
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
    def is_valid(self):
        return all(collection.is_valid for collection in self.rows + self.cols)

    @property
    def rows(self):
        return [self.get_row(x) for x in range(0, len(self))]

    @property
    def cols(self):
        return [self.get_col(x) for x in range(0, len(self))]

    @property
    def subgrids(self):
        return [
            self.get_subgrid(x, y)
            for y in range(0, len(self), 3)
            for x in range(0, len(self), 3)
        ]

    def get_row(self, num):
        return SquareCollection(self[num])

    def get_col(self, num):
        return SquareCollection(
            [self[row][num] for row in range(0, len(self))]
        )

    def get_subgrid(self, x, y):
        left_bound = x//3*3
        top_bound = y//3*3
        rows = [self.get_row(x) for x in range(left_bound, left_bound+3)]
        return Subgrid([row[top_bound:top_bound+3] for row in rows])

    def get_intersection_for_square(self, square):
        return self.get_row(square.x) + \
            self.get_col(square.y) + \
            self.get_subgrid(square.x, square.y)

    def __repr__(self):
        percent_solved = len([s for s in self if s.is_solved]) / len(self)**2
        return F"<{self.__class__.__name__} {percent_solved*100}% Solved>"

    def __str__(self):
        line = '+'.join(['-' * 3] * 3)
        display = []
        for row in self.rows:
            display.append(str(row))
        display.insert(3, line)
        display.insert(7, line)
        return '\n'.join(display)

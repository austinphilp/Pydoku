from square import Square


class SquareCollection(object):
    """
    A one dimmensional collection of square objects
    """
    def __init__(self, squares):
        self._squares = squares

    @property
    def is_valid(self):
        """
        Determine whether this collection is "valid" which is to say that none
        of the values currently populated on the grid violate Sudoku's rules.

        A valid SquareCollection is defined by all squares having at least one
        possible values, with no duplications
        """
        return all(square.is_valid for square in self) and \
            len(self) == (len(set(self)))

    def __add__(self, other):
        """
        Override __add__ to allow for the merging of different square
        collections, whether 1D SquareCollections or 2D Grids
        """
        if isinstance(other, SquareCollection):
            return SquareCollection(self._squares + [s for s in other])
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
    """
    A two dimmensional collection of square objects
    """
    def __iter__(self):
        return (
            self._squares[x][y]
            for x in range(0, len(self))
            for y in range(0, len(self))
        )


class Grid(BaseGrid):
    @classmethod
    def load_from_file(cls, lines):
        """
        Generate a grid from the prepared sudoku puzzles.

        Parameters:
            lines (list) - A list of strs representing an unsolved soduku
            puzzle

        Returns:
            Grid - A Grid instance filled using the data provided by the lines
            argument, replacing instances of 0 with an "unsolved" square.
        """
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
        """
        Determine whether the entire grid is "valid" which is to say that none
        of the values currently populated on the grid violate Sudoku's rules
        """
        return all(collection.is_valid for collection in self.rows + self.cols)

    @property
    def rows(self):
        """
        Returns:
            list(SquareCollection) - A list of Square Collections representing
            all the rows within the grid
        """
        return [self.get_row(x) for x in range(0, len(self))]

    @property
    def cols(self):
        """
        Returns:
            list(SquareCollection) - A list of Square Collections representing
            all the columns within the grid
        """
        return [self.get_col(x) for x in range(0, len(self))]

    @property
    def subgrids(self):
        """
        Returns:
            list(Grid) - A list of Square Collections representing all the
                subgrids (3x3 subsections) within the grid
        """
        return [
            self.get_subgrid(x, y)
            for y in range(0, len(self), 3)
            for x in range(0, len(self), 3)
        ]

    def get_row(self, num):
        """
        Parameters:
            num (int) - the index of the row which you would like to access

        Returns:
            SquareCollection - A Square Collection representing the specified
                row within the grid
        """
        return SquareCollection(self[num])

    def get_col(self, num):
        """
        Parameters:
            num (int) - the index of the column which you would like to access

        Returns:
            SquareCollection - A Square Collection representing the specified
                column within the grid
        """
        return SquareCollection([self[r][num] for r in range(0, len(self))])

    def get_subgrid(self, x, y):
        """
        Parameters:
            x (int) - the x coord of the subgrid which you would like to access
                between 0 and 2.
            y (int) - the y coord of the subgrid which you would like to access
                between 0 and 2

        Returns:
            Grid - A Grid instance representing the subgrid specified by the
                given coordinates
        """
        left_bound = x//3*3
        top_bound = y//3*3
        rows = [self.get_row(x) for x in range(left_bound, left_bound+3)]
        return Grid([row[top_bound:top_bound+3] for row in rows])

    def get_intersection_for_square(self, square):
        """
        An "intersection" of a square in Sudoku is any square which exists in the same row,
        column, or subgrid as the square you are examining. This method will
        return all intersecting squares of a given square.

        Parameters:
            square (Square) - The Square instance whos intersection you would
                like to access

        Returns:
            SquareCollection - A SquareCollection instance representing the all
                the squares that "intersect" with the specified square
        """
        return self.get_row(square.x) + \
            self.get_col(square.y) + \
            self.get_subgrid(square.x, square.y)

    def __repr__(self):
        squares_solved = len([s for s in self if s.is_solved])
        # len(self) will return the number of rows, so we need to square it
        num_of_squares = len(self)**2
        percent_solved = round(squares_solved / num_of_squares, 2)
        return F"<{self.__class__.__name__} {percent_solved*100}% Solved>"

    def __str__(self):
        line = '+'.join(['-' * 3] * 3)
        display = []
        for row in self.rows:
            display.append(str(row))
        display.insert(3, line)
        display.insert(7, line)
        return '\n'.join(display)

from constants import BLANK_SPACE_CHAR


class Square(object):
    def __init__(self, x, y, val):
        self.possibilities = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.x, self.y = x, y
        self.value = val

    @property
    def coord(self):
        """
        Returns:
            tuple(int) - A tuple of two ints representing the x and y
            coordinates of this square respectively
        """
        return (self.x, self.y)

    @property
    def is_solved(self):
        """
        Returns:
            bool - True if there is exactly one possible value for this square
        """
        return len(self.possibilities) == 1

    @property
    def value(self):
        """
        Returns:
            int? - The value of this square if it is solved, otherwise None
        """
        return next(iter(self.possibilities)) if self.is_solved else None

    @value.setter
    def value(self, val):
        """
        Parameters:
            val(int) - The value you wish to give this square, if the given val
            is a blank space character, then no set will be performed
        """
        if val != BLANK_SPACE_CHAR:
            self.possibilities = set([val])

    @property
    def is_valid(self):
        """
        Returns:
            bool - True as long as there is at least one possible value for
                this square.
        """
        return len(self.possibilities) > 0

    def remove_possibility(self, num):
        """
        Remove the given value from the possible values for this square

        Parameters:
            num(int) - This value will be removed from this squares possible
                values.

        """
        if num in self.possibilities:
            self.possibilities.discard(num)
            return self.is_solved
        return False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.value or "*")

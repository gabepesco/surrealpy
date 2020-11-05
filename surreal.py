from sortedcontainers import SortedSet


class Surreal:
    """
    Surreal numbers.
    """

    def __init__(self, real: float, left: SortedSet, right: SortedSet):
        # check that no xl >= any xr
        if not left.isdisjoint(right):
            raise Exception("InvalidSurreal")

        self.real = float(real)
        self.left = left
        self.right = right

    def __str__(self):
        left_set = str(self.left)[10:-1] if self.left else "{∅}"
        right_set = str(self.left)[10:-1] if self.right else "{∅}"
        return f"{self.real} = ({left_set}|{right_set})"

    def __neg__(self):
        return Surreal(-self.real, SortedSet(-xl for xl in self.right), SortedSet(-xr for xr in self.left))

    def __pos__(self):
        if self.real < 0:
            return self.__neg__()
        else:
            return self

    def __invert__(self):
        x = self.real

        if x == 0:
            raise ZeroDivisionError

        if x < 0:
            return -~-self

        # TODO: Implement inversion (1/x).

    def __add__(self, other):
        # Note: the | operator is the union operation

        real = self.real + other.real
        left = SortedSet(xl + other.real for xl in self.left) | SortedSet(yl + self.real for yl in other.left)
        right = SortedSet(xr + other.real for xr in self.right) | SortedSet(yr + self.real for yr in other.right)

        return Surreal(real, left, right)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        x, y = self.real, other.real

        real = x + y
        left = SortedSet(xl * y + x * yl - xl * yl for xl in self.left for yl in other.left) | SortedSet(xr * y + x * yr - xr * yr for xr in self.right for yr in other.left)
        right = SortedSet(xl * y + x * yr - xl * yr for xl in self.left for yr in other.right) | SortedSet(x * yl + xr * y - xr * yl for xr in self.right for yl in other.left)

        return Surreal(real, left, right)

    def __truediv__(self, other):
        # Doesn't work until negation is implemented.
        return self * ~other

    def __lt__(self, other):
        return self <= other and not self == other

    def __le__(self, other):
        x, y = self.real, other.real

        if y > self.left[-1]:
            return False

        elif other.right[-1] > x:
            return False

        return True

    def __eq__(self, other):
        return self.real == other.real and self.left == other.left and self.right == other.right


print(-Surreal(1.0, SortedSet([0]), SortedSet([])))

class Surreal:
    """
    Surreal numbers.
    """

    def __init__(self, real: float, left: frozenset, right: frozenset):
        # check that no xl >= any xr
        if not left.isdisjoint(right):
            raise Exception("Invalid surreal number")

        self.real = real
        self.left = left
        self.right = right

    def __str__(self):
        leftset = str(self.left)[10:-1] if self.left else "{∅}"
        rightset = str(self.left)[10:-1] if self.right else "{∅}"
        return str(self.real) + "=(" + leftset + "|" + rightset + ")"

    def __neg__(self):
        return Surreal(-self.real, frozenset([-xl for xl in self.right]), frozenset([-xr for xr in self.left]))

    def __pos__(self):
        if self.real < 0:
            return self.__neg__()
        else:
            return self

    def __add__(self, other):
        left = frozenset([xl + other.real for xl in self.left]) | frozenset([yl + self.real for yl in other.left])
        right = frozenset([xr + other.real for xr in self.right]) | frozenset(yr + self.real for yr in other.right)
        real = self.real + other.real
        return Surreal(real, left, right)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        pass

    def __lt__(self, other):
        return self <= other and not self == other

    def __le__(self, other):
        for xl in self.left:
            if xl >= other.real:
                return False

        for yr in other.right:
            if yr <= self.real:
                return False

        return True

    def __eq__(self, other):
        return self.real == other.real and self.left == other.left and self.right == other.right

print(-Surreal(1,frozenset([0]),frozenset([])))
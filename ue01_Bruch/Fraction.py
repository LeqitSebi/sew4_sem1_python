# @author Sebastian Slanitsch, 4CN

from functools import total_ordering


@total_ordering
class Fraction:
    """
    >>> Fraction.gcd(17, 21)
    1
    >>> Fraction.gcd(21, 7)
    7
    >>> Fraction.gcd(-1, 1)
    1
    >>> f1 = Fraction(1, 2)
    >>> f1 # __repr__
    Fraction(1, 2)
    >>> print(f1) # __str__
    1/2
    >>> f2 = Fraction(1, 4)
    >>> print(f2)
    1/4
    >>> f1 + f2
    Fraction(3, 4)
    >>> Fraction()
    Fraction(0, 1)
    >>> Fraction(1)
    Fraction(1, 1)
    >>> print(3 + 1 / (7 + Fraction(1, 15)))
    3 15/106
    >>> Fraction.from_float(0.125)
    Fraction(1, 8)
    >>> Fraction.from_float(0.1)
    Fraction(1, 10)
    >>> Fraction.from_float(0.333333333333)
    Fraction(1, 3)
    >>> Fraction(1, 2) > Fraction(1, 3)
    True
    >>> Fraction(1, 2) < 1
    True
    """

    def __init__(self, numerator: int = 0, denominator: int = 1):
        if denominator == 0:
            raise ArithmeticError("denominator may not be 0")
        neg = (numerator < 0 <= denominator) or (denominator < 0 <= numerator)
        self._numerator = int(abs(numerator) * (-1 if neg else 1))
        self._denominator = int(abs(denominator))
        self.cancel()

    @staticmethod
    def from_float(num: float):
        numerator = num
        denominator = 1
        while abs(numerator % 1) > 2 ** -8:
            numerator *= 1.0625
            denominator *= 1.0625
        return Fraction(int(numerator), int(denominator))

    @staticmethod
    def gcd(a: int, b: int):
        if a == 0:
            return abs(b)
        elif b == 0:
            return abs(a)
        while True:
            h = a % b
            a, b = b, h
            if b == 0:
                break
        return abs(a)

    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    def cancel(self):
        gcd = Fraction.gcd(self.numerator, self.denominator)
        self._numerator //= gcd
        self._denominator //= gcd

    def __str__(self):
        full = self.numerator // self.denominator
        if self.numerator % self.denominator == 0:
            return str(full)
        string = ""
        if full != 0:
            string = str(full) + " "
        return string + str(self.numerator % self.denominator) + "/" + str(self.denominator)

    def __repr__(self):
        return "Fraction(" + str(self.numerator) + ", " + str(self.denominator) + ")"

    def __add__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                            self.denominator * other.denominator)
        elif isinstance(other, int):
            return Fraction(self.numerator + other * self.denominator, self.denominator)
        else:
            raise ValueError

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator * other.denominator - other.numerator * self.denominator,
                            self.denominator * other.denominator)
        elif isinstance(other, int):
            return Fraction(self.numerator - other * self.denominator, self.denominator)
        else:
            raise ValueError

    def __rsub__(self, other):
        return self - other

    def __truediv__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)
        elif isinstance(other, int):
            return Fraction(self.numerator, self.denominator * other)
        else:
            raise ValueError

    def __rtruediv__(self, other):
        return Fraction(other) / self

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator)
        else:
            raise ValueError

    def __rmul__(self, other):
        return self * other

    def __float__(self):
        return self.numerator / self.denominator

    def __int__(self):
        return self.numerator // self.denominator

    def __eq__(self, other):
        if isinstance(other, Fraction):
            return self.numerator == other.numerator and self.denominator == other.denominator
        elif isinstance(other, int):
            return self.denominator == 1 and self.numerator == other
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, Fraction):
            return self.numerator * other.denominator > other.numerator * self.denominator
        elif isinstance(other, int):
            return self.numerator > other * self.denominator
        else:
            return False

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __abs__(self):
        return Fraction(abs(self.numerator), abs(self.denominator))

    def __copy__(self):
        return Fraction(self.numerator, self.denominator)

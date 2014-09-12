from xgcd import xgcd

class Mod:
    """
    Class for representing elements of GF(p)
    The member x always maintained in 0 <= x < p.
    """
    def __init__(self, x, p):
        """
        TESTS:
        >>> x = Mod(9, 5)
        >>> x
        Mod(4, 5)
        >>> x = Mod(-3, 5)
        >>> x
        Mod(2, 5)
        """
        self.x = x % p
        self.p = p

    def __repr__(self):
        """
        TESTS:
        >>> x = Mod(2, 5)
        >>> x
        Mod(2, 5)
        """
        return "Mod(%d, %d)" % (self.x, self.p)

    def __str__(self):
        """
        TESTS:
        >>> x = Mod(2, 5)
        >>> print str(x)
        2
        >>> print x
        2
        """
        return str(self.x)

    def __add__(self, other):
        """
        TESTS:
        >>> Mod(2, 5) + Mod(2, 5)
        Mod(4, 5)
        >>> Mod(2, 5) + Mod(4, 5)
        Mod(1, 5)
        >>> Mod(2, 5) + Mod(3, 6)
        Traceback (most recent call last):
        ...
        AssertionError: cannot add Mods of different moduli
        """
        assert other.p == self.p, "cannot add Mods of different moduli"
        x = self.x + other.x
        return Mod(x, self.p)

    def __sub__(self, other):
        """
        TESTS:
        >>> Mod(4, 5) - Mod(2, 5)
        Mod(2, 5)
        >>> Mod(2, 5) - Mod(4, 5)
        Mod(3, 5)
        >>> Mod(2, 5) - Mod(3, 6)
        Traceback (most recent call last):
        ...
        AssertionError: cannot subtract Mods of different moduli
        """
        assert other.p == self.p, "cannot subtract Mods of different moduli"
        x = self.x - other.x
        return Mod(x, self.p)

    def __mul__(self, other):
        return self.coerce_mul(other)

    def coerce_mul(self, other):
        try:
            return self._mul_(other)
        except AttributeError:
            return other.ring(self)._mul_(other)
    def _mul_(self, other):
        """
        TESTS:
        >>> Mod(13, 19) * Mod(5, 19)
        Mod(8, 19)
        >>> Mod(5, 11) * Mod(3, 17)
        Traceback (most recent call last):
        ...
        AssertionError: cannot multiply Mods of different moduli
        """
        assert other.p == self.p, "cannot multiply Mods of different moduli"
        x = self.x * other.x
        return Mod(x, self.p)

    def __invert__(self):
        """
        TESTS:
        >>> ~Mod(5, 19)
        Mod(4, 19)
        """
        y = xgcd(self.x, self.p)
        assert y[0] == 1, 'multiplicative inverse only defined for elements relatively prime to modulus'
        x = y[1]
        return Mod(x, self.p)

    def __neg__(self):
        """
        TESTS:
        >>> -Mod(4, 9)
        Mod(5, 9)
        """
        return Mod(-self.x + self.p, self.p)

    def __div__(self, other):
        """
        TESTS:
        >>> Mod(13, 19) / Mod(5, 19)
        Mod(14, 19)
        >>> Mod(13, 19) / Mod(0, 19)
        Traceback (most recent call last):
        ...
        ZeroDivisionError
        >>> Mod(3, 5) / Mod(1, 5)
        Mod(3, 5)
        """
        if other.x == 0:
            raise ZeroDivisionError
        y = xgcd(other.x, other.p)
        x = self.x * y[1]
        return Mod(x, self.p)

    def __cmp__(self, other):
        """
        >>> Mod(4, 9) < Mod(5, 9)
        True
        >>> Mod(7, 19) < Mod(5, 7)
        Traceback (most recent call last):
        ...
        AssertionError: cannot compare Mods of different moduli
        >>> Mod(5, 7) > Mod(0, 7)
        True
        >>> Mod(88, 88) < Mod(98, 88)
        True
        """
        assert other.p == self.p, "cannot compare Mods of different moduli"
        return cmp(self.x, other.x)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

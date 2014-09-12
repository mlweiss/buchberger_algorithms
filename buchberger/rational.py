def gcd(x, y):
    """
    >>> gcd(1, -2)
    1
    >>> gcd(-1, 2)
    1
    >>> gcd(-3, 0)
    3
    """

    if x < 0:
        x = -x
    if y < 0:
        y = -y
    if y == 0:
        return x
    else:
        return gcd(y, x % y)


def lcm(x,y):

    if x < 0:
        x = -x
    if y < 0:
        y = -y
    if y == 0:
        return x
    else:
        return (x * y) / gcd(x, y)

class Rational:
    def __init__(self, n, d):
        """
        >>> Rational(4, 0)
        Traceback (most recent call last):
        ...
        ZeroDivisionError
        >>> Rational(5, 6)
        Rational(5, 6)
        >>> Rational(6, 9)
        Rational(2, 3)
        """
        if d < 0:
            n = -n
            d = -d
        if d == 0:
            raise ZeroDivisionError
        else:
            g = gcd(n ,d)
            self.n = n / g
            self.d = d / g

    def numerator(self):
        return self.n

    def denominator(self):
        return self.d

    
    def __repr__(self):
        """
        >>> Rational(5, -8)
        Rational(-5, 8)
        """

        return "Rational(%d, %d)" % (self.n, self.d)
    
    def __add__(self, other):
        """
        >>> Rational(1,3) + Rational(1,3)
        Rational(2, 3)
        >>> Rational(4, 5) + Rational(6, 7)
        Rational(58, 35)
        >>> Rational(3, 6) + Rational(3, 4)
        Rational(5, 4)
        >>> Rational(7, 8) + Rational(5, 6)
        Rational(41, 24)
        """

        x = lcm(self.d , other.d)
        temp_other = other.n * (x / other.d)
        temp_self = self.n * (x / self.d)
        y = temp_other + temp_self
        return Rational(y, x)


    def __sub__(self, other):

        """
        >>> Rational(1,3) - Rational(1,3)
        Rational(0, 1)
        >>> Rational(1,4) - Rational(2,3)
        Rational(-5, 12)
        """

        x = lcm(self.d , other.d)
        temp_other = other.n * (x / other.d)
        temp_self = self.n * (x / self.d)
        y = temp_self - temp_other
        return Rational(y, x)

    def __mul__(self, other):
        return self.coerce_mul(other)

    def coerce_mul(self, other):
        try:
            return self._mul_(other)
        except AttributeError:
            return other.ring(self)._mul_(other)
        
    def _mul_(self, other):
        
        """
        >>> Rational(1, 3) * Rational(9, 7)
        Rational(3, 7)
        >>> Rational(4, 5) * Rational(12, 11)
        Rational(48, 55)
        >>> Rational(3, 2) * Rational(-1, 2)
        Rational(-3, 4)
        """

        x = self.n * other.n
        y = self.d * other.d
        return Rational(x, y)
    
    def __invert__(self):

        """
        >>> ~Rational(2, 3)
        Rational(3, 2)
        """

        return Rational(self.d, self.n)

    def __div__(self, other):

        """
        >>> Rational(2, 3) / Rational(3, 4)
        Rational(8, 9)
        >>> Rational(3, 5) / Rational(8, 7)
        Rational(21, 40)
        >>> Rational(1,1) / Rational(0,1)
        Traceback (most recent call last):
        ...
        ZeroDivisionError
        """

        x = self.n * other.d
        y = self.d * other.n
        return Rational(x, y)

    def __cmp__(self, other):
        """
        >>> cmp(Rational(4, 3), 1)
        0
        >>> cmp(Rational(5, 3), 0)
        1
        >>> Rational(5, 3) < Rational(7,4)
        True
        """
        if type(other) == int:
             return cmp(float(self.n/self.d), other) 
        elif isinstance(other, Rational):
            x = lcm(self.d, other.d)
            return cmp((self.n * (x / self.d)), (other.n * (x / other.d)))

    def __neg__(self):
        return Rational(-self.n, self.d)
    
    def __str__(self):
        """
        >>> print Rational(3, 1)
        3
        >>> print Rational(3, 11)
        3/11
        """

        if self.d == 1:
            return str(self.n)
        else:
            x = str(self.n)
            y = str(self.d)
            return x + '/' + y
            
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

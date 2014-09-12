# This is a class that represents multivariate monomials, to be used in conjunction with a polynomial ring class.

from PolynomialRing import PolynomialRing
from CoefficientField import RationalField, PrimeField

class Monomial:
   
    def __init__(self, ring, degrees):
        """
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, ['x','y','z'])
        >>> Monomial(R, (2, 3))
        Traceback (most recent call last):
        AssertionError: Degree vector length should equal number of variables
        """
        self.degrees = tuple(degrees)
        self.ring = ring
        assert self.ring._num_vars == len(self.degrees), 'Degree vector length should equal number of variables'

    def _mul_(self, other):
        """
        >>> from polynomial import *
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, 'x')
        >>> Monomial(R, (1,))
        x
        >>> R = PolynomialRing(QQ, ['x','y','z'])
        >>> Monomial(R, (3, 1, 4)) * Monomial(R, (4, 2, 1))
        x^7*y^3*z^5
        >>> Monomial(R, (8, 8, 1)) * Monomial(R, (4, 5, 3))
        x^12*y^13*z^4
        >>> Monomial(R, (3, 2, 1)) * Monomial(R, (1, 3, 2))
        x^4*y^5*z^3
        >>> J = PolynomialRing(QQ, 'xy')
        >>> Monomial(J, (2, 3)) * Monomial(R, (1, 3, 4))
        Traceback (most recent call last):
        AssertionError: Monomials should be from the same ring
        """
        assert self.ring == other.ring, 'Monomials should be from the same ring'
        x = [self.degrees[i] + other.degrees[i] for i in range(len(self.degrees))]
        return Monomial(self.ring, x)

    def __mul__(self, other):
        return self.coerce_mul(other)
    
    def coerce_mul(self, other):
        try:
            return self._mul_(other)
        except AttributeError:
            return other._mul_(self)
#        except:
#            raise ValueError, 'multiplication of type %s and %s is not supported' %(type(self), type(other))
        
    def is_divisible(self, other):
        """
        >>> R = PolynomialRing('QQ', 'xyz')
        >>> Monomial(R, (2, 1, 3)).is_divisible(Monomial(R, (2, 1, 2)))
        True
        >>> Monomial(R, (2, 1, 1)).is_divisible(Monomial(R, (2, 1, 2)))
        False
        """
        x = [self.degrees[i] - other.degrees[i] for i in range(len(self.degrees))]
        if all([value >= 0 for value in x]):
            return True
        else:
            return False
        
    def __div__(self, other):
        """
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, ['x','y','z'])
        >>> Monomial(R, (4, 5, 1)) / Monomial(R, (3, 2, 0))
        x*y^3*z
        >>> Monomial(R, (1, 0, 0)) / Monomial(R, (0, 0, 0))
        x
        >>> Monomial(R, (2, 2, 2)) / Monomial(R, (3, 1, 1))
        Traceback (most recent call last):   
        ArithmeticError: Monomials with negative exponents are not members of the ring
        """
        x = tuple([self.degrees[i] - other.degrees[i] for i in range(len(self.degrees))])
        for i in range(len(x)):
            if all([power >= 0 for power in x]):
                return Monomial(self.ring, x)
            else:
                raise ArithmeticError, 'Monomials with negative exponents are not members of the ring'

    def __repr__(self):
        """
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, 'x')
        >>> str(Monomial(R, (1,)))
        'x'
        >>> R = PolynomialRing(QQ, ['x','y','z'])
        >>> str(Monomial(R, (0, 0, 1)))
        'z'
        >>> str(Monomial(R, (1, 3, 4)))
        'x*y^3*z^4'
        >>> J = PolynomialRing('QQ', ['n', 'jimmy', 'b', 'g', 'd'])
        >>> str(Monomial(J, (2, 5, 0, 0, 1)))
        'n^2*jimmy^5*d'
        >>> str(Monomial(J, (0, 0, 0, 0, 0)))
        '1'
        """
        x = ''
        if self.degrees == tuple([0*y for y in self.degrees]):
            return '1'
        if self.ring.num_vars() == 1:
            if self.degrees[0] == 1:
                return self.ring.var_list[0]
            else:
                return self.ring.var_list[0] + '^' + str(self.degrees[0])
        for i in range(len(self.degrees)):
            if self.degrees[i] == 0:
                pass
            elif x == '':
                if self.degrees[i] == 1:
                    x += self.ring.var_list[i]  
                else:
                    x += self.ring.var_list[i] + '^' +  str(self.degrees[i])
            else:
                if self.degrees[i] == 1:
                    x += '*' + self.ring.var_list[i]
                else:
                    x += '*' + self.ring.var_list[i] + '^' + str(self.degrees[i])                
        return x

    def __pow__(self, power):

        """
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, ['x','y','z'])
        >>> Monomial(R, (3, 2, 3)) ** 2
        x^6*y^4*z^6
        >>> Monomial(R, (4, 3, 7)) ** 3
        x^12*y^9*z^21
        """
        x = tuple([self.degrees[i] * power for i in range(len(self.degrees))]) 
        return Monomial(self.ring, x)

    def __cmp__(self, other):

        """
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, ['x', 'y', 'z'])
        >>> cmp(Monomial(R, (3, 1, 3)), Monomial(R, (3, 2, 5)))
        -1
        >>> cmp(Monomial(R, (2, 1, 0)), Monomial(R, (1, 5, 5)))
        1
        >>> cmp(Monomial(R, (3, 1, 0)), Monomial(R, (3, 1, 0)))
        0
        """
        return cmp(self.degrees, other.degrees)

    def __getitem__(self, key):

        """
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, ['x','y','z'])
        >>> Monomial(R, (4, 3, 2))[1]
        3
        >>> Monomial(R, (3, 2, 1))[0]
        3
        """
        return self.degrees[key]

    def degree(self):
        
        """
        >>> QQ = RationalField()
        >>> R = PolynomialRing(QQ, ['x','y','z'])
        >>> Monomial(R, (8, 3, 2)).degree()
        13
        >>> Monomial(R, (5, 9, 2)).degree()
        16
        >>> Monomial(R, (3, 5, 12)).degree()
        20
        """
        return sum(self.degrees) 

    def __eq__(self, other):
        """
        >>> R = PolynomialRing('QQ', 'xyz')
        >>> Monomial(R, (0, 4, 2)) == Monomial(R, (0, 4, 2))
        True
        >>> Monomial(R, (0, 4, 2)) == Monomial(R, (0, 4, 3))
        False
        """
        return self.degrees == other.degrees

    def gcd(self, other):
        """
        >>> R = PolynomialRing('QQ', 'xyz') 
        >>> Monomial(R, (4, 1, 0)).gcd(Monomial(R, (3, 2, 0)))
        x^3*y
        >>> Monomial(R, (4, 1, 0)).gcd(Monomial(R, (5, 2, 0)))
        x^4*y
        >>> Monomial(R, (4, 1, 6)).gcd(Monomial(R, (5, 2, 8)))
        x^4*y*z^6
        """
        new = []
        for i,j in zip(self.degrees, other.degrees):
            if i >= j:
                new.append(j)
            else:
                new.append(i)
        return Monomial(self.ring, tuple(new))

    def lcm(self, other):
        """
        >>> R = PolynomialRing('QQ', 'xyz') 
        >>> Monomial(R, (4, 1, 0)).lcm(Monomial(R, (3, 2, 0)))
        x^4*y^2
        """
        return (self * other) / self.gcd(other)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
            

from polynomial import Polynomial
from buchberger import groebner
from PolynomialRing import PolynomialRing
from CoefficientField import RationalField, PrimeField
import sys

def is_groebner(basis):
    """
    TESTS:

    >>> R = PolynomialRing(RationalField(), 'xyz')
    >>> x, y, z = R.variables()
    >>> I = [x**2 + x*y + x + y + 1, x*y*z**2 +  y*z**3 + 1]
    >>> J = groebner(I)
    >>> is_groebner(J)
    True
    """

    for i in range(len(basis)):
        for j in range(len(basis)):
            if j <= (i - 1):
                S = basis[i].S_polynomial(basis[j])
                if  S.divide(basis)[1].is_zero():
                    pass
                else:
                    return False
    return True
                       
                       
if __name__ == '__main__':
    import doctest
    doctest.testmod()

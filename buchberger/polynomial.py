# A polynomial class, to be used in conjunction with the class Monomial and Polynomial Ring, this will contain, add, div, and mul operations for polynomials.

from monomial import Monomial
from polynomial_ring import PolynomialRing
from coefficient_field import RationalField, PrimeField, QQ

class Polynomial:

    def __init__(self, ring,  monomials, coeffs):
        """
        The monomials should be in order and distinct
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> Polynomial(R, [Monomial(R, (1, 3, 1)), Monomial(R, (12, 1, 2)), Monomial(R, (1, 3, 1))], [1, 1, 1])
        Traceback (most recent call last):
        AssertionError: Monomials should be distinct and ordered from least to greatest
        >>> Polynomial(R, [Monomial(R, (0, 0, 1)), Monomial(R, (1, 0, 1)), Monomial(R, (2, 0, 2))], [1, 2, 1])
        x^2*z^2 + 2*x*z + z
        >>> Polynomial(R, [Monomial(R, (0, 0, 3)), Monomial(R, (0, 0, 3)), Monomial(R, (0, 0, 4))], [2, 3, 4])
        Traceback (most recent call last):
        AssertionError: Monomials should be distinct and ordered from least to greatest
        >>> Polynomial(R, [4], [4])
        Traceback (most recent call last):
        AssertionError: Monomial list should only contain monomials
        """
        self.monomials = monomials
        self.ring = ring
        if all([isinstance(coeff, int) for coeff in coeffs]):
            self.coeffs = [self.ring.coeff_ring(coeff) for coeff in coeffs]
        else:
            self.coeffs = coeffs
        assert len(self.coeffs) == len(self.monomials), 'Coefficient list length should equal monomial list length'
        zero = self.ring.coeff_ring(0)
        self.monomials = [self.monomials[i] for i in range(len(self.monomials)) if self.coeffs[i] != zero]
        self.coeffs = [coeff for coeff in self.coeffs if coeff != zero]
        assert all([isinstance(monomial, Monomial) for monomial in self.monomials]), 'Monomial list should only contain monomials'
        assert all([self.monomials[i] < self.monomials[i+1] for i in range(len(self.monomials)-1)]), 'Monomials should be distinct and ordered from least to greatest'
        
    def __repr__(self):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> x + y + z
        x + y + z
        >>> -5*x**12*y*z**5 + (-1)*x**12*y*z**2 + (-1)*x*y**3*z
        (-5)*x^12*y*z^5 + (-1)*x^12*y*z^2 + (-1)*x*y^3*z
        >>> z - z
        0
        >>> R = PolynomialRing(PrimeField(5), 'xyz')
        >>> x, y, z = R.variables()
        >>> x + y + 2*z + 3*z + z
        x + y + z
        """
        L = len(self.monomials)
        x = ''
        if not self.coeffs and not self.monomials:
            return '0'
        if not self.monomials:
            return self.coeffs[0]
        for m, c in zip(reversed(self.monomials), reversed(self.coeffs)):
            if x == '':
                if c == self.ring.coeff_ring(1): # must compare using elements of the ring not python ints
                    x += str(m)
                elif c < self.ring.coeff_ring(0):
                    x += '(%s)*%s' % (c, m)
                elif c == self.ring.coeff_ring(0):
                    pass
                else:
                    x += '%s*%s' % (c, m)
            elif c == self.ring.coeff_ring(1):
                x += ' + %s' % m
            elif c < self.ring.coeff_ring(0):
                x += ' + (%s)*%s' % (c, m)
            elif c == self.ring.coeff_ring(0):
                pass
            else:
                x += ' + %s*%s' % (c, m)
        return x
    
    def __add__(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> (x + z) + (3*y*z + z)
        x + 3*y*z + 2*z
        >>> x + x*y*z**2 + 3*x*y + (-1)*x*y*z**2
        3*x*y + x
        >>> 2*y + x*y + 3*x + 2*x*z + 3*x**2*z**2
        3*x^2*z^2 + x*y + 2*x*z + 3*x + 2*y
        >>> 3*y + x*y**2 + 3
        x*y^2 + 3*y + 3*1
        """
        if not isinstance(other, Polynomial):
            other = self.ring(other)

        i = 0
        j = 0
        monomials = []
        coeffs = []
        L1 = len(self.monomials)
        L2 = len(other.monomials)
        while i < L1 or j < L2:
            if (i < L1 and j < L2) and self.monomials[i] == other.monomials[j]:
                monomials.append(self.monomials[i])
                coeffs.append(self.coeffs[i] + other.coeffs[j])
                i += 1
                j += 1
            elif i == L1 or (j < L2 and self.monomials[i] > other.monomials[j]):
                monomials.append(other.monomials[j])
                coeffs.append(other.coeffs[j])
                j += 1
            else:
                monomials.append(self.monomials[i])
                coeffs.append(self.coeffs[i])
                i += 1
        return Polynomial(self.ring, monomials, coeffs)

    def __radd__(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> 2 + x
        x + 2*1
        >>> x**2 + y**2 + 0
        x^2 + y^2
        >>> Monomial(R, (0, 1, 1)) + z
        y*z + z
        """
        return self + other
    
    def __sub__(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> 2*x + 2*x*y*z**2 - 3*x -3*x*y
        2*x*y*z^2 + (-3)*x*y + (-1)*x
        >>> 2*x + x*y*z**2 - 3*x*y - x*y*z**2
        (-3)*x*y + 2*x
        """
        if not isinstance(other, Polynomial):
            other = self.ring(other)

        i = 0
        j = 0
        monomials = []
        coeffs = []
        L1 = len(self.monomials)
        L2 = len(other.monomials)
        while i < L1 or j < L2:
            if (i < L1 and j < L2) and self.monomials[i] == other.monomials[j]:
                monomials.append(self.monomials[i])
                coeffs.append(self.coeffs[i] - other.coeffs[j])
                i += 1
                j += 1
            elif i == L1 or (j < L2 and self.monomials[i] > other.monomials[j]):
                monomials.append(other.monomials[j])
                coeffs.append(-other.coeffs[j])
                j += 1
            else:
                monomials.append(self.monomials[i])
                coeffs.append(self.coeffs[i])
                i += 1
        return Polynomial(self.ring, monomials, coeffs)   

    def __rsub__(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> 2 - x
        (-1)*x + 2*1
        >>> Monomial(R, (4, 3, 180)) - x**7
        (-1)*x^7 + x^4*y^3*z^180
        """
        return -self + other
    
    def cub_mul(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> (2*x + 2*x*y*z**2).cub_mul(3*x*y - x*y*z**2)
        (-2)*x^2*y^2*z^4 + 6*x^2*y^2*z^2 + (-2)*x^2*y*z^2 + 6*x^2*y
        >>> (2*x*y + x*y*z**2).cub_mul(3*x*y + x*y*z**2)
        x^2*y^2*z^4 + 5*x^2*y^2*z^2 + 6*x^2*y^2
        >>> (y + x).cub_mul(y + x)
        x^2 + 2*x*y + y^2
        >>> (x + y + z).cub_mul(x + y + z)
        x^2 + 2*x*y + 2*x*z + y^2 + 2*y*z + z^2
        """
        x = Polynomial(self.ring, [], [])
        L1 = len(self.monomials)
        L2 = len(other.monomials)
        for i in range(L1):
            for j in range(L2):
                monomials = self.monomials[i] * other.monomials[j]
                coeffs = self.coeffs[i] * other.coeffs[j]
                x += Polynomial(self.ring, [monomials], [coeffs])
        return x

    def _mul_(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> y * (y*z + z)
        y^2*z + y*z
        >>> (x + y) * (x + y)
        x^2 + 2*x*y + y^2
        >>> (x*y*z + x**2*y + x**3*y**2*z**3) * (x*y + x**2*y)
        x^5*y^3*z^3 + x^4*y^3*z^3 + x^4*y^2 + x^3*y^2*z + x^3*y^2 + x^2*y^2*z
        >>> R = PolynomialRing(QQ, 'x')
        >>> x = R.variables()
        >>> x**2
        x^2
        >>> 2*x**2
        2*x^2
        >>> x**2 * 0
        0
        """
        if not isinstance(other, Polynomial):
            other = self.ring(other)

        f = self
        g = other
        if len(f.monomials) < len(g.monomials):
            f,g = g,f
        L1, L2 = len(f.monomials), len(g.monomials)

        if not L2:
            return Polynomial(self.ring, [], [])
        elif L2 == 1:
            return Polynomial(self.ring, [m * g.monomials[0] for m in f.monomials], [m * g.coeffs[0] for m in f.coeffs])
        else:
            h1 = g.monomials[:L2/2]
            h2 = g.monomials[L2/2:]
            c1 = g.coeffs[:L2/2]
            c2 = g.coeffs[L2/2:]
            return f * Polynomial(self.ring, h1, c1) + f * Polynomial(self.ring, h2, c2)

    def __mul__(self, other):
        return self.coerce_mul(other)

    def coerce_mul(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> (x).coerce_mul(QQ(4))
        4*x
        >>> (QQ(4)).coerce_mul(x)
        4*x
        """
        try:
            return other.ring(self)._mul_(other)
        except:
            return self.ring(other)._mul_(self)
        else:
            raise ValueError, 'multiplication of type %s and %s is not supported' %(type(self), type(other))
        
    def __rmul__(self, other):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> QQ(4) * x**2
        4*x^2
        >>> Monomial(R, (0, 4, 0)) * x**2
        x^2*y^4
        >>> F7 = PrimeField(7)
        >>> x, y, z = PolynomialRing(F7, 'xyz').variables()
        >>> F7(5) * x**2*y**2*z**25
        5*x^2*y^2*z^25
        """
    
        return self * other
    
    def divide(self, divisors):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> (x**2*y + x*y**2 + y**2).divide([x*y + (-1), y**2 - 1])
        ([x + y, 1], x + y + 1)
        >>> (x*y**2 + 1).divide([x*y + 1, y + 1])
        ([y, (-1)*1], 2*1)
        >>> (x**2*y + x*y**2 + y**2).divide([y**2 - 1, x*y -1])
        ([x + 1, x], 2*x + 1)
        >>> (x**2*y + x*y**2 + y**2).divide([x**4*y**2*z**2])
        ([0], x^2*y + x*y^2 + y^2)
        >>> (3*x).divide([x])
        ([3*1], 0)
        >>> (x**2).divide([R(0)])
        Traceback (most recent call last):
        ZeroDivisionError
        """
        if all([not divisors[i].monomials and not divisors[i].coeffs for i in range(len(divisors))]):
            raise ZeroDivisionError
        if not all([isinstance(divisor, Polynomial) for divisor in divisors]): # maybe change this to an error
            divisors = [self.ring(divisor) for divisor in divisors]

        p = Polynomial(self.ring, self.monomials[:], self.coeffs[:])
        quots = [Polynomial(self.ring, [], []) for divisor in divisors]
        r = Polynomial(self.ring, [], [])
        while p.monomials:
            i = 0
            division_occurred = False
            while i < len(divisors) and not division_occurred:
                LM_i = divisors[i].monomials[-1]
                LM_p = p.monomials[-1]
                LC_i = divisors[i].coeffs[-1]
                LC_p = p.coeffs[-1]
#                print 'LM_i = %s; LM_p = %s; LC_i = %s; LC_p = %s; p = %s; quots = %s; i = %s' %(LM_i, LM_p, LC_i, LC_p, p, quots, i)
                if LM_p.is_divisible(LM_i):
                    quots[i].monomials.append(LM_p / LM_i)
                    quots[i].coeffs.append(LC_p / LC_i)
                    p = p - (Polynomial(self.ring, [LM_p / LM_i], [LC_p / LC_i]) * divisors[i])
                    division_occurred = True
                else:
                    i += 1
            if not division_occurred:
                r.monomials.append(p.monomials.pop())
                r.coeffs.append(p.coeffs.pop())
        for i in range(len(quots)): 
            quots[i].monomials = list(reversed(quots[i].monomials))
            quots[i].coeffs = list(reversed(quots[i].coeffs))
        return quots, Polynomial(self.ring, list(reversed(r.monomials)), list(reversed(r.coeffs)))
                    
    def __pow__(self, power):
        """
        >>> from polynomial import *
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> x**2
        x^2
        >>> 
        x^4*z^2 + 2*x^4*z + x^4
        >>> Polynomial(R, [Monomial(R, (2, 0, 0)), Monomial(R, (2, 0, 1))], [1, 1])**0
        1
        >>> Polynomial(R, [Monomial(R, (2, 0, 0)), Monomial(R, (2, 0, 1))], [1, 1])**1
        x^2*z + x^2
        >>> Polynomial(R, [Monomial(R, (0, 1, 0)), Monomial(R, (1, 0, 0))], [1, 1])**3
        x^3 + 3*x^2*y + 3*x*y^2 + y^3
        >>> Polynomial(R, [Monomial(R, (1, 1, 1))], [1])**5
        x^5*y^5*z^5
        """
        i = 0
        x = Polynomial(self.ring, self.monomials, self.coeffs)
        if power == 0:
            return Polynomial(self.ring, [Monomial(self.ring, (0, 0, 0))], [1]) 
        elif power == 1:
            return self
        else:
            for i in range(power-1):
                x = x * self
            return x
    
    def LM(self):
        """
        A function that returns the leading monomial of a polynomial

        TESTS:
        
        >>> R = PolynomialRing(QQ, 'xyz')        
        >>> x, y, z = R.variables()
        >>> f = x**2 + y**2 + z**2
        >>> f.LM()
        x^2
        >>> (x**3 + x*y + (-3)*y*z).LM()
        x^3
        >>> (x - x).LM()
        0
        """

        if self.is_zero():
            return Polynomial(self.ring, [], [])
        else:
            return self.monomials[-1]

    def LT(self):
        """
        A function that returns the leading term of a polynomial

        TESTS:
        
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> f = x**3 * y**4 + x**3 * y**4 + x + y
        >>> f.LT()
        2*x^3*y^4
        >>> (R(0)).LT()
        0
        """
        if self.is_zero():
            return Polynomial(self.ring, [], [])
        else:
            return Polynomial(self.ring, [self.LM()], [self.coeffs[-1]])

    def LC(self):
        """
        Returns the leading coefficient of a polynomial

        TESTS:
        
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> f = 2*x**3 + 2*y**4 + x + y
        >>> f.LC()
        Rational(2, 1)
        >>> (3*f).LC()
        Rational(6, 1)
        >>> (R(0)).LC()
        Rational(0, 1)
        """
        
        if self.is_zero():
            return self.ring.coeff_ring(0)
#            return Polynomial(self.ring, [], [])
        else:
            return self.coeffs[-1]
#            return Polynomial(self.ring, [Monomial(self.ring, tuple([0 for var in self.ring.var_list]))], [self.coeffs[-1]])
        
    def __neg__(self):
        """
        Returns a the additive inverse of a polynomial
        """
        return Polynomial(self.ring, self.monomials, [-coeff for coeff in self.coeffs])

    def LC_is_one(self):
        """
        Tests whether a polynomial's leading coefficient is 1

        TESTS:
        
        >>> from rational import *
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> f = 2*x**3 + 2*y**4 + x + y
        >>> f.LC_is_one()
        False
        >>> (Rational(1, 2) * f).LC_is_one()
        True
        >>> (R(0)).LC_is_one()
        False
        """
        if not self.monomials and not self.coeffs:
            return False
        else:
            return self.coeffs[-1] == 1
        
    def is_zero(self):
        """
        Tests whether a polynomial is the zero polynomial, returns Boolean variable

        TESTS:

        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> (x**3).is_zero()
        False
        >>> Polynomial(R, [], []).is_zero()
        True
        >>> (x - x).is_zero()
        True
        >>> (R(0)).is_zero()
        True
        """
        if not self.monomials and not self.coeffs:
            return True
        else:
            return False
            
    def S_polynomial(self, other):
        """
        Returns the S_polynomial of two polynomials

        TESTS:
        
        >>> R = PolynomialRing(QQ, 'xyz')        
        >>> x, y, z = R.variables()
        >>> (x**3 * y**2 - x**2 * y**3 + x).S_polynomial(x**4 * y + x**4 * y + x**4 * y + y**2)
        (-1)*x^3*y^3 + x^2 + (-1/3)*y^3
        >>> (x**3 - (x*y + x*y)).S_polynomial(-x**2)
        (-2)*x*y
        >>> (x**3 - 2*x*y).S_polynomial(x**2*y - 2*y**2 + x)
        (-1)*x^2
        >>> (x**3).S_polynomial(R(0))
        0
        """

        zero = self.ring(0)
        if self.is_zero() or other.is_zero():
            return zero
        else:
            LCM = self.LM().lcm(other.LM())
            s_f = Polynomial(self.ring, [LCM / self.LM()], [self.ring.coeff_ring(1) / self.LT().coeffs[0]])
            s_g = Polynomial(other.ring, [LCM / other.LM()], [other.ring.coeff_ring(1) / other.LT().coeffs[0]])
            return s_f * self - s_g * other
        
    def __eq__(self, other):
        """
        Tests the equality of two polynomials
        """
        return self.monomials == other.monomials and self.coeffs == other.coeffs
#        try: 
#        except AttributeError:
#            return self.monomials == self.ring(other).monomials and self.coeffs == self.ring(other).coeffs
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()


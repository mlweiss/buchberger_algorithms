# This is a class that represents a multivariate polynomial ring, it relies on the multivariate monomial class, monomial.py

from coefficient_field import RationalField, PrimeField, QQ
from random import randint


class PolynomialRing:

    def __init__(self, coeff_ring, var_list): 
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> R.var_list
        ['x', 'y', 'z']
        """
        from monomial import Monomial
        self.coeff_ring = coeff_ring
        self._num_vars = len(var_list)
        if isinstance(var_list, list):
            self.var_list = var_list
        elif isinstance(var_list, str):
            self.var_list = [var for var in var_list]
        else:
            raise TypeError, 'variable list must either be list or a string'

    def __call__(self, element):
        """
        >>> from polynomial import *
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> R(2)
        2*1
        >>> R(Monomial(R, (4, 3, 2))) # this fails since monomial is not imported at the top-level in PolynomialRing 
        x^4*y^3*z^2
        """
        from polynomial import Polynomial
        from mod import Mod
        from rational import Rational
        from monomial import Monomial
        
        if isinstance(element, Polynomial):
            if element.ring is self:
                return element
            else: 
                for i in range(len(element.monomials)):
                    element.monomials[i].ring = self
                return Polynomial(self, element.monomials, [self(coeff) for coeff in element.coeffs]) 
        elif isinstance(element, Monomial): 
            return Polynomial(self, [element], [self.coeff_ring(1)])
        elif isinstance(element, Mod) or isinstance(element, Rational) or isinstance(element, int):
            return Polynomial(self, [Monomial(self, tuple([0 for var in self.var_list]))], [self.coeff_ring(element)])
        
    def num_vars(self):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> R.num_vars()
        3
        """
        return self._num_vars

    def __repr__(self):
        """
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> R
        Polynomial Ring in 3 variable(s), x, y, z over QQ
        """
        y = ''
        for i in range(len(self.var_list)):
            if i == 0:
                y += self.var_list[i]
            else:
                y += ', ' + self.var_list[i]
        return 'Polynomial Ring in ' + str(len(self.var_list)) + ' variable(s), ' + y + ' over ' + str(self.coeff_ring)

    def variables(self):
        """
        Creates pointers to polynomial variables
        >>> R = PolynomialRing(QQ, 'xyz')
        >>> x, y, z = R.variables()
        >>> x**2 + y**2
        x^2 + y^2
        >>> R = PolynomialRing(QQ, 'x')
        >>> x = R.variables()
        >>> x
        x
        """
        from polynomial import Polynomial
        from monomial import Monomial
        variables = []
        if self.num_vars() == 1:
            return Polynomial(self, [Monomial(self, (1,))], [1])
        for i in range(len(self.var_list)):
            degree = [0 for j in range(self.num_vars())]
            degree[i] = 1
            variables.append(Polynomial(self, [Monomial(self, tuple(degree))], [1]))
        return tuple(variables)

    def random_monomial(self, degree):
        """
        Returns a random monomial of degree <= 'degree'
        """
        from monomial import Monomial
        while True:
            m = [randint(0, degree) for i in range(self._num_vars)]
            if sum(m) <= degree:
                return Monomial(self, tuple(m))
            

    def random(self, degree, num_terms):
        """
        Returns a random polynomial of degree at most `degree' with at most `num_terms' terms
        """
        from polynomial import Polynomial
        num_terms = randint(1, num_terms)
        monomials = [self.random_monomial(degree) for i in range(num_terms)]
        coeffs = [self.coeff_ring.random_element() for i in range(num_terms)]
        L = zip(monomials, coeffs)
        L.sort()
        monomials = [L[0][0]]
        coeffs = [L[0][1]]
        zero = self.coeff_ring(0)
        for i in range(1, len(L)):
            m, c = L[i]
            m_prev = L[i-1][0]
            if m != m_prev and c != zero:
                monomials.append(m)
                coeffs.append(c)
        return Polynomial(self, monomials, coeffs)


# Uncomment to use lexicographical ordering of monomials    
#class PolyLex(PolynomialRing):
                
 #   def __cmp__(m1, m2):
  #      """
   #     >>> cmp(PolyLex(Monomial([2,3])), PolyLex(Monomial([0, 3, 4, 5])))
        -1
    #    """
        
     #   return cmp(m1.polynomial, m2.polynomial)

class PolyGrlex(PolynomialRing):
    
    def __cmp__(m1, m2):
       """
       >>> from monomial import Monomial
       >>> R = PolyGrlex(QQ, 'xyz')
       >>> cmp(Monomial(R, (1, 6, 7)), Monomial(R, (1, 6, 2)))
       1
       >>> cmp(Monomial(R, (2, 3, 4)), Monomial(R, (4, 6, 2)))
       -1
       >>> cmp(PolyGrlex(Monomial([1, 1, 1, 5])), PolyGrlex(Monomial([1, 1, 1, 4, 1])))
       1
       """
       x = m1 / m2
       if sum(m1.polynomial) != sum(m2.polynomial):
           return cmp(sum(m1.polynomial),sum(m2.polynomial))
       else:
           for i in range(len(x.degrees)):
               if x[i] == 0:
                   i += 1
               if x[i] < 0:
                   return -1
               else:
                   return 1
# Uncomment to use reverse lexicographical ordering of monomials.   
#class PolyGrevlex(PolynomialRing):
    
 #   def __cmp__(m1, m2):
 #       """
 #       >>> cmp(PolyGrevlex(Monomial([2, 3])), PolyGrevlex(Monomial([1, 6])))
 #       -1
 #       >>> cmp(PolyGrevlex(Monomial([2, 3, 4])), PolyGrevlex(Monomial([1, 6])))
 #       1
 #       >>> cmp(PolyGrevlex(Monomial([1, 1, 1, 5])), PolyGrevlex(Monomial([1, 1, 1, 4, 1])))
 #       1
 #       >>> cmp(PolyGrevlex(Monomial([1, 5, 2])), PolyGrevlex(Monomial([4, 1, 3])))
 #       1
 #       """
 #       x = m1.polynomial / m2.polynomial
  #      i = len(x.degrees) - 1
   #     if sum(m1.polynomial) != sum(m2.polynomial):
    #        return cmp(sum(m1.polynomial),sum(m2.polynomial))
    #    else:
    #        while i in range(len(x.degrees)):
     #           if x[i] == 0:
      #              i -= 1
       #         if x[i] < 0:
        #            return 1
         #       else:
          #          return -1
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

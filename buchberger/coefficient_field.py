from rational import Rational
from mod import Mod
from random import randint

class RationalField:
    def __call__(self, x):
        if isinstance(x, Rational):
            return x
        elif isinstance(x, int):
            return Rational(x, 1)
        else:
            raise ValueError, "cannot coerce into rational field"

    def __repr__(self):
        return 'QQ'

class PrimeField:

    def __init__(self, p):
        self.p = p
        
    def __call__(self, x):
        """
        >>> F7 = PrimeField(7)
        >>> x = F7(6)
        >>> x
        Mod(6, 7)
        >>> x + F7(3)
        Mod(2, 7)
        >>> F5 = PrimeField(5)
        >>> F5(F7(6))
        Mod(1, 5)
        """

        if isinstance(x, Mod) and self.p == x.p:
            return x
        elif isinstance(x, Mod):
            return Mod(x.x, min(self.p, x.p))
        elif isinstance(x, int):
            return Mod(x, self.p)
        else:
            raise ValueError, "cannot coerce into prime field"

    def __repr__(self):
        return 'GF(%s)' %self.p

    def random_element(self):
        """
        >>> 
        """
        return Mod(randint(0, self.p - 1), self.p)
    
QQ = RationalField()
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
            

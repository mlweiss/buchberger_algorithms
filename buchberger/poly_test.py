from polynomial_ring import *
from polynomial import *
from time import time

R = PolynomialRing('x')

n = 50

f = Polynomial([Monomial(R, (i,)) for i in range(n)], [1 for i in range(n)])
g = Polynomial([Monomial(R, (n*i,)) for i in range(n)], [1 for i in range(n)])
#print f
#print g

t1 = time()
h = f * g
#print h
t2 = time()
print "using fast mul took %f seconds" % (t2 - t1)

t1 = time()
h = f.cub_mul(g)
t2 = time()
print "using slow mul took %f seconds" % (t2 - t1)
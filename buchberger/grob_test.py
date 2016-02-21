from polynomial import *
from buchberger import groebner
from grob_check import is_groebner
from random import seed, randint
import timeit

seed(559)

K = PrimeField(5)
R = PolynomialRing(K, 'xy')

max_degree = 5
max_terms = 7

for trial in range(10000):
	num_polys = randint(2, max_terms)
	I = [R.random(max_degree, max_terms) for i in range(num_polys)]
	I = [poly for poly in I if len(poly.coeffs)]
	J = groebner(I)
	test = is_groebner(J)
	assert test
	if trial % 50 == 0:
		print trial


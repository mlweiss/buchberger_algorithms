from polynomial import *
from buchberger import *

R = PolynomialRing(QQ, 'xyz')
x, y, z = R.variables()


groebner([x**2 - 2*x*y, x**2*y - 2*y**2 + x])

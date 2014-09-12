from polynomial import Polynomial

def groebner(poly_list):
    """
    Takes a list of polynomials from the same ring and returns a Groebner basis

    TESTS:

    >>> from polynomial import *
    >>> R = PolynomialRing(QQ, 'xyz')
    >>> x, y, z = R.variables()
    >>> F = [x - 2*x*y, x**3*y - 2*x**2 + y]
    >>> groebner(F)
    [x^3 + (-2)*x*y, x^2*y + x + (-2)*y^2, x^2, 2*x*y, (-1)*x + 2*y^2, (-4)*y^3]
    """

    n = len(poly_list)
    ideal = poly_list[:]
    changed = True
    while changed:
        changed = False
        for i in range(len(ideal)):
            for j in range(len(ideal)):
                if j <= (i - 1):
                    S = (ideal[i].S_polynomial(ideal[j])).divide(ideal)[1]
                    if not S.is_zero():
#                        print 'i = '+str(ideal[i]), 'j =' + str(ideal[j]), 'S polynomial = %s, S remainder = %s' %(ideal[i].S_polynomial(ideal[j]), S)
                        ideal.append(S)
                        changed = True
                if changed:
                    break
            if changed:
                break
    return ideal
                                                                                                                                                                


if __name__ == '__main__':
    import doctest
    doctest.testmod()

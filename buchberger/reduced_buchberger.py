def groebner_red(poly_list):
    """
    Takes an ordered list of polynomials from the same ring and returns a reduced Groebner basis

    TESTS:

    >>> from polynomial import *
    >>> R = PolynomialRing(QQ, 'xyz')
    >>> x, y, z = R.variables()
    >>> F = [x**3 - 2*x*y, x**2*y - 2*y**2 + x]
    >>> groebner_red(F)
    [x^3 + (-2)*x*y, x^2*y + x + (-2)*y^2, x^2, x*y, x + (-2)*y^2, y^2]
    """

    n = len(poly_list)
    assert all([poly_list[i] > poly_list[i+1] for i in range(n - 1)]), 'Polynomials should be ordered from greatest to least greatest'
    ideal = poly_list[:]
    changed = True
    for poly in ideal:
        poly = poly * ~poly.LC()
    while changed:
        changed = False
        for i in range(len(ideal)):
            for j in range(len(ideal)):
                if j <= (i - 1):
                    S = (ideal[i].S_polynomial(ideal[j])).divide(ideal)[1]
                    if not S.is_zero():
                        S = ~S.LC() * S
                        for poly in reversed(ideal):
                            if poly < S:
                                S_index = ideal.index(poly) + 1
                                ideal.insert(S_index, S)
                                break
                        for n in range(S_index):
                            for monomial in S.monomials:
                                if monomial in ideal[n].monomials:
                                    vanishing_coeff = ideal[n].coeffs[ideal[n].monomials.index(monomial)]
                                    ideal[n] = ideal[n] - vanishing_coeff * S
                            if len(ideal[n].monomials) == 1 and len(S.monomials) == 1:
                                if ideal[n].divide([S])[1] == ideal[n].ring(0):
                                    ideal.pop(n)
                        changed = True
                if changed:
                    break
            if changed:
                break
    return ideal
                                                                                                                                                                


if __name__ == '__main__':
    import doctest
    doctest.testmod()

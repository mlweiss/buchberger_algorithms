def xgcd(a, b):
    """
    # returns answer in the form (gcd, x1, y1) where gcd(x, y) = x* x1 + y * y1, for the moment xgcd may return a negative gcd for negative input        
    >>> xgcd(30, 18)
    (6, -1, 2)
    >>> xgcd(18, 30)
    (6, 2, -1)
    >>> xgcd(2, -1)
    (1, 1, 1)
    """

    x = 0
    y = 1
    lastx = 1
    lasty = 0
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lastx) = (lastx - q * x, x)
        (y, lasty) = (lasty - q * y, y)
    return (a, lastx, lasty)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

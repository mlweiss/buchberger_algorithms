def gcd(a, b):

    """
        >>> gcd(3,-1)
        1
        >>> gcd(16, 0)
        16
        >>> gcd(7843, 29)
        1
    """
    if b == 0:
        return a
    r = a % b
    while r != 0:
        a = b
        b = r
    if b < 0:
        b = - b
    return b

 
if __name__ == '__main__':
    import doctest
    doctest.testmod()
            

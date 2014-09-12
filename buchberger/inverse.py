from xgcd import *
    
def inverse(x, m):
    """
    >>> inverse(99, 100)
    'Mod(99,100)'
    """
  
    y = xgcd(x, m)
    n = y[2]
    if n < 0:
        n += m
    return 'Mod(n, m)'

if __name__ == '__main__':
    import doctest
    doctest.testmod()

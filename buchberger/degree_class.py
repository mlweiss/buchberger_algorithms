class Degree:

    def __init__(self, degrees):
        self.degrees = degrees

    def __repr__(self, degrees):
        return 'Monomial(' + repr(self.degrees) + ')'
    
    def degree(self, degrees):
        """
        >>> degree(Monomial((3,2,2)))
        (3, 2, 2)
        """
        return self.degrees


if __name__ == '__main__':
    import doctest
    doctest.testmod()

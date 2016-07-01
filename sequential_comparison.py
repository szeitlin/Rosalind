__author__ = 'szeitlin'

import operator

def longest_overlap(counts1, counts2):
    """
    Helper for compare_base_counts. Compares compressed base count lists in both
    orientations (1,2 and 2,1)

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: count (int) of maximum number of overlapping bases at the ends


    >>> longest_overlap(['A1', 'T1'], ['T1', 'C1'])
    1
    >>> longest_overlap(['A3', 'T1', 'A4'], ['T1', 'A4', 'T1', 'C3'])
    2
    >>> longest_overlap(['A4', 'G2', 'A1', 'C4'], ['T4', 'C3', 'A4', 'G2', 'A1'])
    3
    >>> longest_overlap(['G3', 'T3'], ['A3', 'G3'])
    1
    """




if __name__=='__main__':
    import doctest
    doctest.testmod()


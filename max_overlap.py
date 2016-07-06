__author__ = 'szeitlin'

import numpy as np

def max_overlap(one, two, debug=False):
    """
    Find the diagonal of the comparison matrix with the maximum overlap

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: tuple of offset, max overlap
    """
    if one == two:
        return

    a = np.array([x for x in one[1]])
    b = np.vstack([x for x in two[1]])
    compared = a==b

    #find the diagonal with the most (sequential*) Truthiness on the ends*

    max_diag = max(len(a), len(b))

    bestsofar = (0,0)

    for i in range(max_diag):
        endsmatch = np.diagonal(compared, offset=i)
        #print("above {}".format(endsmatch))

        maxhere = count_sequential(list(endsmatch))
        #print(maxhere)

        if maxhere > bestsofar[1]:
            bestsofar = (i, maxhere)

        #print(bestsofar)

        otherendsmatch = np.diagonal(compared, offset=-i)
        #print("below {}".format(otherendsmatch))

        maxthere = count_sequential(list(otherendsmatch))
        #print(maxthere)

        if maxthere > bestsofar[1]:
            bestsofar = (-i, maxthere)

        #print(bestsofar)

    return bestsofar


def count_sequential(listofbool):
    """
    Easy to count total True values using built-in on list.
    This counts longest sequential run of True values.

    >>> count_sequential([True, True, True, False])
    3
    >>> count_sequential([True, True, True, False, True, True])
    3
    >>> count_sequential([True, True, True, True])
    4

    """
    count = 0
    max_seq = 0

    if len(listofbool) > 0:
        if listofbool[0] == False: #must match on the ends
            return 0

        else:
            for x in listofbool:
                if x!=True:
                    max_seq = count
                    count = 0
                elif x==True:
                    count += 1

            max_seq = count

            return max_seq

    else:
        return 0

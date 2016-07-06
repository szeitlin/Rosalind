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

    #find the diagonal with the most (sequential) Truthiness

    max_diag = max(len(a), len(b))

    bestsofar = (0,0)

    for i in range(max_diag):
        endsmatch = np.diagonal(compared, offset=i)
        #print("above {}".format(endsmatch))

        maxhere = list(endsmatch).count(True)
        #print(maxhere)

        if maxhere > bestsofar[1]:
            bestsofar = (i, maxhere)

        #print(bestsofar)

        otherendsmatch = np.diagonal(compared, offset=-i)
        #print("below {}".format(otherendsmatch))

        maxthere = list(otherendsmatch).count(True)
        #print(maxthere)

        if maxthere > bestsofar[1]:
            bestsofar = (-i, maxthere)

        #print(bestsofar)

    return bestsofar





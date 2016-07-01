__author__ = 'szeitlin'

import numpy as np

from gc_content import parse_data

def get_o3_overlap(one, two, debug=False):
    """
    Instead of using base_counts to get maximum overlap,
    just score the overlap of the 3 end bases.

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: overlap score (int)
    """
    if one == two:
        return

    a = np.array([x for x in one[1]])
    b = np.vstack([x for x in two[1]])
    compared = a==b

    offset = len(a) - 3 #3 is the length of overlap we want
    endsmatch = np.diagonal(compared, offset=-(offset-1)) #not sure about this one

    if len(endsmatch) != 3:
        return

    elif endsmatch.all() == True:
        if debug==True:
            return (two, one)
        else:
            return (two[0], one[0])

    otherendsmatch = np.diagonal(compared, offset=offset)

    if len(otherendsmatch) != 3:
        return

    elif otherendsmatch.all() == True:
        if debug==True:
            return (one, two)
        else:
            return (one[0], two[0])

    else:
        return

def compare_all_pairs_both_ways(labeled):
    """
    This needs revision to deal with duplicates and self-matches.

    :param labeled:
    :return:
    """
    whole_list = labeled.copy()
    matches = []

    while len(labeled) >=1:

        current = labeled.pop()
        #print("current is {}".format(current))

        for i in range(len(whole_list)):
            x = whole_list[i]
            #print("comparing to {}".format(x))

            result = get_o3_overlap(current, x)
            if result is not None:
                if result not in matches:
                    matches.append(result)

    #print(matches)

    return matches

if __name__=='__main__':
    # import doctest
    # doctest.testmod()

    with open('rosalind_grph.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))

    matches = compare_all_pairs_both_ways(labeled)


    #to make a graph with Gephi:
    with open("overlaps.csv", 'w') as results:
        for item in matches:
            results.write("{} {}\n".format(item[0], item[1]))
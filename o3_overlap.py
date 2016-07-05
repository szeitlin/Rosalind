__author__ = 'szeitlin'

import numpy as np
import itertools

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
    otheroffset = len(b) - 3
    endsmatch = np.diagonal(compared, offset=otheroffset)
    otherendsmatch = np.diagonal(compared, offset=offset)

    if len(endsmatch) != 3:
        return

    elif (len(endsmatch) == 3) and (endsmatch.all() == True):
        if debug==True:
            return (one[1], two[1])
        else:
            return (one[0], two[0])

    if len(otherendsmatch) != 3:
        return

    elif (len(otherendsmatch) == 3) and (otherendsmatch.all() == True):
        if debug==True:
            return (two[1], one[1])
        else:
            return (two[0], one[0])

    else:
        return

def compare_all_pairs_both_ways(labeled):
    """
    This is a little slower because it's doing
    10100 instead of 10000.

    :param labeled: list of tuples (name, seq)
    :return: list of tuples (name, name) of matches
    """

    whole_list = labeled.copy()
    matches = []

    while len(labeled) >=1:

        current = labeled.pop()

        #print("current is {}".format(current))

        for i in range(len(whole_list)):
            x = whole_list[i]

            #print("comparing to {}".format(x))

            result = get_o3_overlap(current, x, debug=True)
            if result is not None:
                if result not in matches:
                    matches.append(result)

    return matches

def itertools_combinations(labeled):
    """
    Try this to do all 100,000 comparisons.

    :param labeled:
    :return:
    """
    matches = []

    pairs = itertools.permutations(labeled, 2) #all possible orderings
    for pair in list(pairs):
        result = get_o3_overlap(pair[0], pair[1], debug=True)
        if result is not None:
            if result not in matches:
                matches.append(result)

    return matches

def get_all_ends(labeled):
    """
    helper for making sure all possible matches are identified

    :param labeled: list of name, seq
    :return: dict of {last three bases (str): counts}
    """
    enddict = dict()
    frontdict = dict()

    for item in labeled:
        front = item[1][0:3]
        end = item[1][-3::]
        if front not in frontdict:
            frontdict[front]= 1
        elif front in frontdict:
            frontdict[front] +=1
        if end not in enddict:
            enddict[end] = 1
        elif end in enddict:
            enddict[end] +=1

    print(frontdict)
    print(enddict)

    paircount = 0
    for x,y in zip(sorted(frontdict), sorted(enddict)):
        #some more sophisticated checking here
        #if key x == key y:
            # if x.value > 1 or y.value > 1:
            #     make a pair
            #     subtract 1 from each and
            #     keep whatever's leftover for further comparisons' \
            # otherwise if x.value == 1 and y.value == 1:
            #     make a pair

    return paircount





if __name__=='__main__':
    # import doctest
    # doctest.testmod()

    with open('rosalind_grph.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))
    expected_pairs = get_all_ends(labeled)

    #matches = compare_all_pairs_both_ways(labeled)

    matches = itertools_combinations(labeled)

    if len(matches) != expected_pairs:
        print("warning! expected {} but only found {}".format(expected_pairs, len(matches)))

    #to make a graph with Gephi:
    with open("overlaps.csv", 'w') as results:
        for item in matches:
            results.write("{};{}\n".format(item[0], item[1]))
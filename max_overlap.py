__author__ = 'szeitlin'

from collections import defaultdict
import numpy as np

from gc_content import parse_data
from o3_overlap import matches_to_rosalind, matches_to_graph

def max_overlap(one, two):
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

        maxhere = count_sequential(list(endsmatch))

        if maxhere > bestsofar[1]:
            bestsofar = (i, maxhere)

        otherendsmatch = np.diagonal(compared, offset=-i)

        maxthere = count_sequential(list(otherendsmatch))

        if maxthere > bestsofar[1]:
            bestsofar = (-i, maxthere)

    return one, two, bestsofar

def count_sequential(listofbool):
    """
    Helper for max_overlap.
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

def compare_all_pairs_both_ways(labeled, debug=False):
    """
    :param labeled: list of tuples (name, seq)
    :return: adjacency dict
    {(name,seq): [list of ((name,seq), (offset, overlap)) tuples]}
    """

    whole_list = labeled.copy()
    matches = defaultdict(list)

    while len(labeled) >=1:

        current = labeled.pop()

        for i in range(len(whole_list)):
            x = whole_list[i]

            result = max_overlap(current, x)

            #avoid getting duplicates!
            if result is not None:
                if result[0] not in matches:
                    matches[result[0]].append((result[1], result[2]))
                elif result[0] in matches:
                    if result[1] not in matches[result[0]]:
                        matches[result[0]].append((result[1], result[2]))

    if debug==True:
        for k,v in matches.items():
            print(k[0], [(x[0][0],x[1]) for x in v])

    return matches


if __name__=='__main__':

    with open('CENPA_3chunks.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))
    expected_pairs=3

    matches = compare_all_pairs_both_ways(labeled, debug=True)

    #matches = itertools_combinations(labeled)

    if len(matches) != expected_pairs:
        print("warning! expected {} but found {}".format(expected_pairs, len(matches)))

    #to make a graph with Gephi:
    matches_to_graph(matches)

    #to make results file for Rosalind
    matches_to_rosalind(matches)
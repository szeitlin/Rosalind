__author__ = 'szeitlin'

from collections import defaultdict
import operator
from gc_content import parse_data

def get_o3_overlap(one, two):
    """
    Instead of using base_counts to get maximum overlap,
    just score the overlap of the 3 end bases.

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: overlap score (int)
    """
    i = -1
    scorelist = []

    one_len = len(one[1])
    two_len = len(two[1])

    for j in range(3):
        if one[1][i] != two[1][j]:
            if any([x > 0 for x in scorelist]):
                break
            else:
                #penalty for mismatches, otherwise just get similarity
                scorelist.append(-1)

        elif one[1][i] == two[1][j]:
            scorelist.append(1)

    return sum(scorelist)

def get_o3_scores(labeled, debug=False):
    """
    Score matches using only the overlap of the 3 end bases.
    Keep only those with score of 3 (the max).

    :param labeled: list of (name,seq) pairs
    :return: score_dict
    """
    score_dict = dict()

    whole_list = labeled.copy()

    while len(labeled) >= 1:

        current = labeled.pop(0)

        for i in range(len(whole_list)):
            x = whole_list[i]

            score1 = get_o3_overlap(current, x)
            score2 = get_o3_overlap(x, current)

            if score1 == 3:
                score_dict[(current[0],x[0])] = score1
            if score2 == 3:
                score_dict[(x[0], current[0])] = score2

    if debug==True:
        return score_dict
    else:
        return list(score_dict.keys())


if __name__=='__main__':
    # import doctest
    # doctest.testmod()

    with open('rosalind_grph.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))
    scored = get_o3_scores(labeled)

    #to make a graph with Gephi:
    with open("overlaps.csv", 'w') as results:
        for item in scored:
            results.write("{} {}\n".format(item[0], item[1]))
__author__ = 'szeitlin'

import numpy as np

from gc_content import parse_data

def get_o3_overlap(one, two):
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

    endsmatch = np.diagonal(compared, offset=-4) #offset may require calculation?

    if endsmatch.all() == True:
        print(one[0], two[0])

    otherendsmatch = np.diagonal(compared, offset=3)

    if otherendsmatch.all() == True:
        print(two[0], one[0]) #will have to check on direction

    else:
        print(" ")

def compare_all_pairs_both_ways(labeled):
    """
    This needs revision to deal with duplicates and self-matches.

    :param labeled:
    :return:
    """
    whole_list = labeled.copy()

    while len(labeled) >=1:

        current = labeled.pop()
        #print("current is {}".format(current))

        for i in range(len(whole_list)):
            x = whole_list[i]
            #print("comparing to {}".format(x))

            get_o3_overlap(current, x)



if __name__=='__main__':
    # import doctest
    # doctest.testmod()

    with open('overlap_sample.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))

    compare_all_pairs_both_ways(labeled)


    # #to make a graph with Gephi:
    # with open("overlaps.csv", 'w') as results:
    #     for item in scored:
    #         results.write("{} {}\n".format(item[0], item[1]))
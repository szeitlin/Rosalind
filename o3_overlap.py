__author__ = 'szeitlin'

import numpy as np
from collections import defaultdict
import itertools

from gc_content import parse_data



def just_check_ends(one, two):
    front1 = one[1][0:3]
    end1 = one[1][-3:]
    front2 = two[1][0:3]
    end2 = two[1][-3:]

    if end1==front2:
        return (one, two)
    elif end2 == front1:
        return (two, one)
    else:
        return

def compare_all_pairs_both_ways(labeled, debug=False):
    """
    This is a little slower because it's doing
    10100 instead of 10000.

    :param labeled: list of tuples (name, seq)
    :return: adjacency dict of {(name,seq): [list of (name,seq) tuples]}
    """

    whole_list = labeled.copy()
    matches = defaultdict(list)

    while len(labeled) >=1:

        current = labeled.pop()

        #print("current is {}".format(current))

        for i in range(len(whole_list)):
            x = whole_list[i]

            #print("comparing to {}".format(x))

            #result = get_o3_overlap(current, x, debug=True)
            result = just_check_ends(current, x)

            #avoid getting duplicates!
            if result is not None:
                if result[0] not in matches:
                    matches[result[0]].append(result[1])
                elif result[0] in matches:
                    if result[1] not in matches[result[0]]:
                        matches[result[0]].append(result[1])

    if debug==True:
        for item in matches:
            print(item[1], [x[1] for x in matches[item]])

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
        #result = get_o3_overlap(pair[0], pair[1], debug=True)
        result = just_check_ends(pair[0], pair[1])
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
        end = item[1][-3:]
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

    for key in frontdict.keys():
        if key in enddict:
            paircount += frontdict[key] & enddict[key]

    return paircount


def matches_to_graph(matches):
    """
    extract pairs from adjacency dict, and write sequences to a file

    :param matches: adjacency dict of sequences (str): [list of str]
    :return: pairs formatted for Gephi, i.e. node1;node2 (separated by
    semicolon, 1 pair per line)
    """
    with open("overlaps.csv", 'w') as results:
        for item in matches:
            for val in matches[item]:
                if item[0] != val[0]: #check for directed loops
                    results.write("{};{}\n".format(item[1], val[1]))

def matches_to_rosalind(matches):
    """
    extract pairs from adjacency dict,
    remove any directed loops (nodes that point to themselves)
    and write names to a file

    :param matches: adjacency dict of {(name,seq): [list of (name,seq) tuples]}
    :return: pairs formatted for Rosalind, i.e. node1 name only node2 name only
    (separated by 1 space, 1 pair per line)
    """
    with open("overlaps.txt", 'w') as results:
        for item in matches:
            for val in matches[item]:
                if item[0] != val[0]: #check for directed loops
                    results.write("{} {}\n".format(item[0], val[0]))


if __name__=='__main__':
    # import doctest
    # doctest.testmod()

    with open('rosalind_grph_9_dataset.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))
    expected_pairs = get_all_ends(labeled)

    matches = compare_all_pairs_both_ways(labeled, debug=True)

    #matches = itertools_combinations(labeled)

    if len(matches) != expected_pairs:
        print("warning! expected {} but found {}".format(expected_pairs, len(matches)))

    #to make a graph with Gephi:
    matches_to_graph(matches)

    #to make results file for Rosalind
    matches_to_rosalind(matches)

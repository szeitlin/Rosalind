__author__ = 'szeitlin'

from collections import defaultdict
import numpy as np

from gc_content import parse_data
from o3_overlap import matches_to_rosalind, matches_to_graph
from max_overlap import compare_all_pairs_both_ways

class Node:
    def __init__(self, match):
        self.name = match[0][0]
        self.seq = match[0][1]
        self.neighbors_list = match[1]

    def get_left_neighbor(self):
        """
        Given a node, return the
        best match to the left (if present)
        otherwise return None

        :param node:
        :return: node or None

        >>> get_left_neighbor(('first', [('second', (60, 31)), ('third', (21, 3))]))
        None
        >>> get_left_neighbor(('second', [('first', (-60, 31)), ('third', (60, 31))]))
        ('first')
        >>> order_neighbors(('third', [('first', (-21, 3)), ('second', (-60, 31))]))
        ('second')
        """
        #within neighbors_list, 2nd half of tuple is (offset, overlap)
        #compare magnitude of overlap
        neighbors = self.neighbors_list

        best_left = (None, 0)

        for x,y in neighbors:
            if y[1] < 0:
                if y[1] < best_left[1]:
                    best_left = (x, y)

        self.left_neighbor = best_left[0]

        return


class Edge:
    def __init__(self, node1,  node2):
        self.nodes = (node1, node2)

class Graph:
    def __init__(self, listofedges):
        self.edges = listofedges








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
__author__ = 'szeitlin'

from collections import defaultdict
import numpy as np

from gc_content import parse_data
from o3_overlap import matches_to_rosalind, matches_to_graph
from max_overlap import compare_all_pairs_both_ways

class Node:
    def __init__(self, name, seq):
        self.name = name
        self.seq = seq

    def get_left_neighbor(self, neighbors_list):
        """
        Given a node, return the
        best match to the left (if present)
        otherwise return None

        :param node:
        :return: node or None

        >>> get_left_neighbor(('first', [('second', (60, 31)), ('third', (21, 3))]))
        None
        >>> get_left_neighbor(('second', [('first', (-60, 31)), ('third', (60, 31))]))
        'first'
        >>> get_left_neighbor(('third', [('first', (-21, 3)), ('second', (-60, 31))]))
        'second'
        """
        #within neighbors_list, 2nd half of tuple is (offset, overlap)
        #compare magnitude of overlap

        best_left = (None, 0)

        for x,y in neighbors_list:
            if y[0] < 0:     #negative sign indicates that it's on the left
                if y[1] < best_left[1]:
                    best_left = (x, y)

        try:
            self.left_neighbor = Node(best_left[0][0], best_left[0][1])
        except TypeError as e: #there may not be one
            self.left_neighbor = None
        return


    def get_right_neighbor(self, neighbors_list):
        """
        Given a node, return the
        best match to the left (if present)
        otherwise return None

        :param node:
        :return: node or None

        >>> get_right_neighbor(('first', 'CGAT'),[('second', 'ACCG'), (60, 31), \
                                (('third', 'GGTC'), (21, 3))]))
        'second'
        >>> get_right_neighbor(('second', 'ACCG'),[(('first', 'CGAT'), (-60, 31)), \
                                (('third', 'GGTC'), (60, 31))]))
        'third'
        >>> get_right_neighbor(('third', 'GGTC'), [(('first', 'CGAT'), (-21, 3)), \
                                (('second', 'ACCG'), (-60, 31))]))
        None
        """
        print(neighbors_list)

        best_right = (None, 0)

        for x,y in neighbors_list:
            if y[0] > 0:     #positive sign indicates that it's on the right
                print('overlap {} vs. bestsofar {}'.format(y[1], best_right[1]))
                if y[1] > best_right[1]:
                    best_right = (x, y)

        try:
            self.right_neighbor = Node(best_right[0][0], best_right[0][1])
        except TypeError as e:
            self.right_neighbor = None
        return


class Edge:
    def __init__(self, node):
        self.left_edge = (node, node.left_neighbor)
        #self.right_edge = (node, node.right_neighbor)

    def __str__(self):
        print(self.left_edge)
        #print(self.right_edge)

class Graph:
    def __init__(self, listofedges):
        self.edges = listofedges

    def flatten_graph(self):
        pass


def nodemaker(matches):
    """
    Generate nodes from list of matches.
    :param matches: adjacency dict {(name,seq): [list of (name,seq) tuples]}
    :return: yield one node at a time
    """
    for match in matches.items():
        name = match[0][0]
        seq = match[0][1]
        neighbors_list = match[1]
        newnode = Node(name, seq)
        newnode.get_left_neighbor(neighbors_list)
        newnode.get_right_neighbor(neighbors_list)
        yield newnode

def edgemaker(matches):
    """
    Generate edges from nodes and their neighbors

    :return: yield one edge at a time
    """
    nodes = nodemaker(matches)

    while nodes:
        try:
            newnode = next(nodes)
            newedge = Edge(newnode)
            yield newedge

        except StopIteration:
            break

def make_listofedges(matches):
    """
    Create listofedges from edges.
    :return:
    """
    listofedges = []
    edges = edgemaker(matches)

    while edges:
        try:
            newedge = next(edges)
            listofedges.append(newedge)
        except StopIteration:
            break

    return listofedges



if __name__=='__main__':

    with open('CENPA_3chunks.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))
    expected_pairs=3

    matches = compare_all_pairs_both_ways(labeled)
    print(matches)

    if len(matches) != expected_pairs:
        print("warning! expected {} but found {}"
              .format(expected_pairs, len(matches)))



    #to make a graph with Gephi:
    matches_to_graph(matches)

    #to make results file for Rosalind
    matches_to_rosalind(matches)
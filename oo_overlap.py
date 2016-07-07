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
        #print(neighbors_list)

        best_right = (None, 0)

        for x,y in neighbors_list:
            if y[0] > 0:     #positive sign indicates that it's on the right
                if y[1] > best_right[1]:
                    best_right = (x, y[1])

        try:
            self.right_neighbor = Node(best_right[0][0], best_right[0][1])
        except TypeError as e:
            self.right_neighbor = Node("end", None)
        return


class Edge:

    def __init__(self, node):
        self.right_edge = (node, node.right_neighbor)
        self.tail = node
        self.head = node.right_neighbor

    def __str__(self):
        return "node {}, right_neighbor {}".format(
                self.right_edge[0].name, self.right_edge[1].name)

    def get_node_overlap(self, matches):
        """
        Retrieve overlap length from matches dict.

        :param matches: adjacency dict
        :param self: use node and right_neighbor names for lookup
        :return: int

        >>> get_node_overlap(matches)
        31

        """
        for k in matches:
            if self.right_edge[0].name in k:
                for val in matches[k]:
                    if self.right_edge[0].name in val[0]:
                        self.overlap = val[1][1]
            else:
                #this means it's the end of the sequence, or an error
                return 0

class Graph:

    def __init__(self, listofedges):
        self.edges = listofedges

    def sort_edges(self, findthis='end'):
        """
        Order and simplify the singly-linked list of edges
        back down to a list of single nodes identified by name.
        """
        edgelist = self.edges
        order = []

        for i in range(len(edgelist)):
            for edge in edgelist:
                #print("item: {}, findthis: {}".format(edge, findthis))
                if findthis == edge.head.name:
                    #print("found!")
                    if findthis not in order:
                        order.insert(0, findthis)
                    findthis = edge.tail.name

                    if len(edgelist) == 1:
                        if edgelist[0].tail.name not in order:
                            order.insert(0, edgelist[0].tail.name)
                    else:
                        edgelist.remove(edge)

        self.nodes_in_order = order

    def flatten_graph(self):
        """ Use the overlap values to align sequences """
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

    if len(matches) != expected_pairs:
        print("warning! expected {} but found {}"
              .format(expected_pairs, len(matches)))

    #to make a graph with Gephi:
    matches_to_graph(matches)

    #to make results file for Rosalind
    matches_to_rosalind(matches)
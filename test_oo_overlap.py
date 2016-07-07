__author__ = 'szeitlin'

import unittest

from max_overlap import compare_all_pairs_both_ways

from gc_content import parse_data

from oo_overlap import (Node, Edge, Graph,
                        make_listofedges,
                        edgemaker,
                        nodemaker)


class TestThreeNodes(unittest.TestCase):

    def setUp(cls):
        with open('CENPA_3chunks.txt', 'r') as f:
            data = f.readlines()

        cls.labeled = list(parse_data(data))

    def test_create_node_from_matches_dict(self):
        self.matches = compare_all_pairs_both_ways(self.labeled)
        firstnode = self.matches.popitem()
        testnode = Node(firstnode[0][0], firstnode[0][1])
        self.assertIn(testnode.name, ['first', 'second', 'third'])

    def test_get_right_neighbor(self):
        self.matches = compare_all_pairs_both_ways(self.labeled)
        firstnode = self.matches.popitem()
        testnode = Node(firstnode[0][0], firstnode[0][1])
        neighbors_list = firstnode[1]
        testnode.get_right_neighbor(neighbors_list)
        self.assertIn(testnode.right_neighbor.name, ['end', 'third', 'second'])

class TestNodePipe(unittest.TestCase):

    def setUp(cls):
        with open('CENPA_3chunks.txt', 'r') as f:
            data = f.readlines()

        labeled = list(parse_data(data))
        cls.matches = compare_all_pairs_both_ways(labeled)

    def test_nodemaker(self):
        nodes = nodemaker(self.matches)
        testnode = next(nodes)
        self.assertIn(testnode.right_neighbor.name, ['end', 'third', 'second'])

class TestEdges(unittest.TestCase):

    def setUp(cls):
        with open('CENPA_3chunks.txt', 'r') as f:
            data = f.readlines()

        labeled = list(parse_data(data))
        cls.matches = compare_all_pairs_both_ways(labeled)

    def test_get_node_overlap(self):
        edges = edgemaker(self.matches)
        newedge = next(edges)
        overlap = newedge.get_node_overlap(self.matches)
        self.assertTrue(isinstance(overlap, int))

    def test_listofedges(self):
        listofedges = make_listofedges(self.matches)
        expected = sorted(['node second, right_neighbor third',
                    'node third, right_neighbor end',
                    'node first, right_neighbor second'
                   ])
        self.assertEqual(expected, sorted([x.__str__() for x in listofedges]))

class TestGraph(unittest.TestCase):

    def setUp(cls):
        with open('CENPA_3chunks.txt', 'r') as f:
            data = f.readlines()

        labeled = list(parse_data(data))
        cls.matches = compare_all_pairs_both_ways(labeled)

        with open('CENPA_8chunks.txt', 'r') as g:
            big_data = g.readlines()

        longer = list(parse_data(big_data))
        cls.more_matches = compare_all_pairs_both_ways(longer)

        with open('CA_superstring3_expected.txt', 'r') as h:
            cls.ss = h.readline().strip()

        with open('CA_superstring8_expected.txt', 'r') as m:
            lines = m.readlines()
            cls.ss8 = ''.join([x.strip() for x in lines])

    def test_sort_edges(self):
        listofedges = make_listofedges(self.matches)
        newgraph = Graph(listofedges)
        self.assertTrue(isinstance(newgraph, Graph))
        newgraph.sort_edges()
        self.assertTrue(isinstance(newgraph.nodes_in_order, list))
        expected = ['first', 'second', 'third', 'end']
        self.assertEqual(newgraph.nodes_in_order, expected)

    def test_flatten_graph(self):
        self.maxDiff = None
        listofedges = make_listofedges(self.matches)
        newgraph = Graph(listofedges)
        newgraph.sort_edges()
        superstring = newgraph.flatten_graph(self.matches)
        self.assertEqual(len(superstring), 180)
        self.assertEqual(self.ss, superstring)

    def test_bigger_graph(self):
        self.maxDiff = None
        listofedges = make_listofedges(self.more_matches)
        self.assertEqual(len(listofedges), 8)
        newgraph = Graph(listofedges)
        newgraph.sort_edges()
        superstring = newgraph.flatten_graph(self.more_matches)
        self.assertEqual(len(superstring), 459)
        self.assertEqual(self.ss8, superstring)

class TestParser(unittest.TestCase):

    def setUp(cls):
        with open('overlap_sample.txt', 'r') as f:
            cls.data = f.readlines()

        with open('rosalind_grph.txt', 'r') as f:
            cls.big_data = f.readlines()

    def test_old_parser(self):
        parsed = list(parse_data(self.big_data))
        self.assertEqual(len(parsed), 100)


if __name__=='__main__':
    unittest.main()
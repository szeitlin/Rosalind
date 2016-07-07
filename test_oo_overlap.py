__author__ = 'szeitlin'

import unittest

from max_overlap import compare_all_pairs_both_ways

from gc_content import parse_data

from oo_overlap import Node, Edge, Graph, make_listofedges, nodemaker


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

    def test_listofedges(self):
        listofedges = make_listofedges(self.matches)
        expected = ['node second, right_neighbor third',
                    'node third, right_neighbor end',
                    'node first, right_neighbor second'
                   ]
        self.assertEqual(expected, [x.__str__() for x in listofedges])

if __name__=='__main__':
    unittest.main()
__author__ = 'szeitlin'

import unittest

from max_overlap import compare_all_pairs_both_ways

from gc_content import parse_data

from oo_overlap import Node, Edge, Graph


class TestNode(unittest.TestCase):

    def setUp(cls):
        with open('CENPA_3chunks.txt', 'r') as f:
            data = f.readlines()

        labeled = list(parse_data(data))
        cls.matches = compare_all_pairs_both_ways(labeled)

    def test_create_node_from_matches_dict(self):
        firstnode = self.matches.popitem()
        testnode = Node(firstnode)
        self.assertIn(testnode.name, ['first', 'second', 'third'])

    def test_get_left_neighbor(self):
        firstnode = self.matches.popitem()
        testnode = Node(firstnode)
        testnode.get_left_neighbor()
        self.assertIn(testnode.left_neighbor, [None, 'first', 'second'])


if __name__=='__main__':
    unittest.main()
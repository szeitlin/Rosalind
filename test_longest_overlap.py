__author__ = 'szeitlin'

import unittest
from overlap import parse_nodes

from gc_content import parse_data

from max_overlap import max_overlap


import operator

class TestMultipleOverlap(unittest.TestCase):

    def setUp(cls):
        with open('overlap_sample.txt', 'r') as f:
            cls.data = f.readlines()

        with open('rosalind_grph.txt', 'r') as f:
            cls.big_data = f.readlines()

    def test_known_3bp_overlap(self):
        a= ('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCT')
        b = ('b', 'CCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGA')
        self.assertEqual(max_overlap(a, b), (57, 3))

    def test_known_longer_overlap(self):
        a =('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAA')
        b = ('b', 'GGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGG')
        self.assertEqual(max_overlap(a, b), (60,24))

class TestMaxOverlap(unittest.TestCase):

    def test_two_short(self):
        a = ('a',  "ATTAGACCTG")
        b = ('b', "AGACCTGCCG")
        self.assertEqual(max_overlap(a, b), (3,7))


if __name__=='__main__':
    unittest.main()

__author__ = 'szeitlin'

import unittest

from max_overlap import max_overlap


class TestMaxOverlap(unittest.TestCase):

    def test_two_short(self):
        a = ('a',  "ATTAGACCTG")
        b = ('b', "AGACCTGCCG")
        actual = max_overlap(a, b)
        self.assertEqual(actual[2], (3,7))

    def test_known_3bp_overlap(self):
        a = ('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCT')
        b = ('b', 'CCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGA')
        actual = max_overlap(a,b)
        self.assertEqual(actual[2], (57, 3))

    def test_known_longer_overlap(self):
        a =('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAA')
        b = ('b', 'GGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGG')
        actual = max_overlap(a, b)
        self.assertEqual(actual[2], (60,24))


if __name__=='__main__':
    unittest.main()

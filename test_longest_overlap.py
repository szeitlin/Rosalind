__author__ = 'szeitlin'

import unittest

from gc_content import parse_data

from max_overlap import max_overlap

from gc_content import parse_data

class TestMultipleAlign(unittest.TestCase):

    def setUp(cls):
        with open('CENPA_3chunks.txt', 'r') as f:
            cls.data = f.readlines()

        with open('CENPA_8chunks.txt', 'r') as f:
            cls.medium = f.readlines()

        with open('CENPA_allchunks.txt', 'r') as f:
            cls.big_data = f.readlines()

        with open('CENPA_mismatched.txt', r) as f:
            cls.nomatch = f.readlines()

    def test_three_chunks(self):
        parsed = list(parse_data(self.data))
        pass

    def test_eightchunks(self):
        parsed = list(parse_data(self.medium))
        pass

    def test_allchunks(self):
        parsed = list(parse_data(self.big_data))
        pass

    def test_falsepositive(self):
        """
        should not match
        """
        parsed = list(parse_data(self.nomatch))
        pass


class TestMaxOverlap(unittest.TestCase):

    def test_two_short(self):
        a = ('a',  "ATTAGACCTG")
        b = ('b', "AGACCTGCCG")
        self.assertEqual(max_overlap(a, b), (3,7))

    def test_known_3bp_overlap(self):
        a= ('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCT')
        b = ('b', 'CCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGA')
        self.assertEqual(max_overlap(a, b), (57, 3))

    def test_known_longer_overlap(self):
        a =('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAA')
        b = ('b', 'GGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGG')
        self.assertEqual(max_overlap(a, b), (60,24))


if __name__=='__main__':
    unittest.main()

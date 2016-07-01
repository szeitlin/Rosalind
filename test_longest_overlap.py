__author__ = 'szeitlin'

import unittest
from overlap import (overlap,
                     base_counts,
                     directional,
                     parse_nodes,
                     compare_base_counts,
                     make_score_dict,
                     pick_best_matches,
                     get_base_counts)

from gc_content import parse_data

from o3_overlap import get_o3_overlap
from sequential_comparison import longest_overlap

import operator

class TestMultipleOverlap(unittest.TestCase):

    def setUp(cls):
        with open('overlap_sample.txt', 'r') as f:
            cls.data = f.readlines()

        with open('rosalind_grph.txt', 'r') as f:
            cls.big_data = f.readlines()

    def test_shorter_longer(self):
        labeled = parse_nodes(self.data)
        a = labeled[0]
        b = labeled[1]
        counts1, counts2 = get_base_counts(a,b)
        lengths = {tuple(counts1): len(counts1), tuple(counts2): len(counts2)}
        shorter, longer = [x[0] for x in sorted(lengths.items(), key=operator.itemgetter(1))]
        self.assertLess(len(shorter), len(longer))

    def test_bigger_shorter_longer(self):
        labeled = list(parse_data(self.big_data))
        a = labeled[0]
        b = labeled[1]
        counts1, counts2 = get_base_counts(a,b)
        lengths = {tuple(counts1): len(counts1), tuple(counts2): len(counts2)}
        shorter, longer = [x[0] for x in sorted(lengths.items(), key=operator.itemgetter(1))]
        self.assertLess(len(shorter), len(longer))

    def test_known_3bp_overlap(self):
        a= ('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCT')
        b = ('b', 'CCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGA')
        counts1 = get_o3_overlap(a, b)
        counts2 = get_o3_overlap(b, a)
        self.assertEqual(counts1, 1)
        self.assertEqual(counts2, 0)

    def test_known_longer_overlap(self):
        a =('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAA')
        b = ('b', 'GGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGG')
        counts1, counts2 = get_base_counts(a, b)
        forward, reverse = longest_overlap(counts1, counts2)
        self.assertGreater(forward, 1, msg= reverse)

    @unittest.skip("not working")
    def test_make_score_dict_entry(self):
        labeled = parse_nodes(self.data)
        whole_list = labeled.copy()
        current = labeled.pop(0)
        x = whole_list[1]
        counts1, counts2 = get_base_counts(current, x)
        forward, reverse = longest_overlap(counts1, counts2)
        self.assertEqual(forward, 1)

if __name__=='__main__':
    unittest.main()

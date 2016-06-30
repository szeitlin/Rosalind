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

    def test_make_score_dict(self):
        labeled = parse_nodes(self.data)
        scored = make_score_dict(labeled, debug=True)
        self.assertEqual(scored, {})

if __name__=='__main__':
    unittest.main()

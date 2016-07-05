__author__ = 'szeitlin'

import unittest

from o3_overlap import get_o3_overlap, compare_all_pairs_both_ways

from overlap import (overlap,
                     base_counts,
                     directional,
                     parse_nodes,
                     compare_base_counts,
                     make_score_dict,
                     pick_best_matches,
                     get_base_counts)

from gc_content import parse_data

class TestScorer(unittest.TestCase):

    def setUp(cls):
        with open('overlap_sample.txt', 'r') as f:
            cls.data = f.readlines()

        with open('rosalind_grph.txt', 'r') as f:
            cls.big_data = f.readlines()


    def test_get_o3_matches_short_seq(self):
        self.longMessage = True #for debugging without truncation
        labeled = parse_nodes(self.data)
        #print(labeled)
        actual = compare_all_pairs_both_ways(labeled)
        expected = [('Rosalind_2391', 'Rosalind_2323'),
                    ('Rosalind_0498', 'Rosalind_2391'),
                    ('Rosalind_0498', 'Rosalind_0442')]
        self.assertEqual(set(expected), set(actual), msg='{0},{1}'.format(expected, actual))

    def test_get_o3_match_long_seq(self):
        a= ('a', 'ACCGAGCGCCACCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCT')
        b = ('b', 'CCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGA')
        result = get_o3_overlap(a, b)
        self.assertEqual(result, ('a', 'b'))

    def test_get_o3_match_known_longer_overlap(self):
        a =('a', 'GAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAG')
        b = ('b', 'GGTCGAGCTGGACGG')
        result = get_o3_overlap(a, b)
        self.assertEqual(result, None)

class TestItertoolsCombinations(unittest.TestCase):

    def get_pairs_returns_expected_number(self):
        pass


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

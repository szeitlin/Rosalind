__author__ = 'szeitlin'

import unittest

from o3_overlap import get_o3_scores, get_o3_overlap

from overlap import (overlap,
                     base_counts,
                     directional,
                     parse_nodes,
                     compare_multiple,
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

    def test_compare_multiple_old(self):
        self.longMessage = True #for debugging without truncation
        labeled = parse_nodes(self.data)
        actual = compare_multiple(labeled)
        expected = [('Rosalind_0498', 'Rosalind_2391'), ('Rosalind_2391', 'Rosalind_2323'), ('Rosalind_0498', 'Rosalind_0442')]
        self.assertEqual(set(expected), set(actual), msg='{0},{1}'.format(expected, actual))

    def test_get_o3_scores_short(self):
        self.longMessage = True #for debugging without truncation
        labeled = parse_nodes(self.data)
        print(labeled)
        actual = get_o3_overlap(labeled)
        expected = [('Rosalind_2391', 'Rosalind_2323'),
                    ('Rosalind_0498', 'Rosalind_2391'),
                    ('Rosalind_0498', 'Rosalind_0442')]
        self.assertEqual(set(expected), set(actual), msg='{0},{1}'.format(expected, actual))

    def test_get_o3_scores_long(self):
        self.longMessage = True #for debugging without truncation
        labeled = list(parse_data(self.big_data))
        score_dict = get_o3_scores(labeled)
        self.assertEqual(len(score_dict), 203)
        self.assertEqual(len(labeled), 0)
        self.assertEqual(len(score_dict), len(set(score_dict))) #no duplicate edges

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

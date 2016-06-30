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

class TestSingleOverlap(unittest.TestCase):

    def setUp(cls):
        cls.one = "AAATAAA"
        cls.two = "AAATTTT"
        cls.three = ('Rosalind_2391', 'AAATTTT')
        cls.four = ('Rosalind_0498', 'AAATAAA')

    def test_overlap_bool(self):
        self.assertTrue(overlap(self.one, self.two))

    def test_base_counts(self):
        self.assertEqual(base_counts(self.one), ['A3', 'T1', 'A3'])

    def test_directional_overlap(self):
        self.assertEqual(directional(self.three, self.four), ('Rosalind_0498', 'Rosalind_2391'))

class TestMultipleOverlap(unittest.TestCase):

    def setUp(cls):
        with open('overlap_sample.txt', 'r') as f:
            cls.data = f.readlines()

        with open('rosalind_grph.txt', 'r') as f:
            cls.big_data = f.readlines()


    def test_parse_nodes(self):
        self.assertEqual(parse_nodes(self.data), [('Rosalind_0498', 'AAATAAA'),
                                                     ('Rosalind_2391', 'AAATTTT'),
                                                     ('Rosalind_2323', 'TTTTCCC'),
                                                     ('Rosalind_0442', 'AAATCCC'),
                                                     ('Rosalind_5013', 'GGGTGGG')])

    def test_compare_multiple(self):
        self.longMessage = True #for debugging without truncation
        labeled = parse_nodes(self.data)
        actual = compare_multiple(labeled)
        expected = [('Rosalind_0498', 'Rosalind_2391'), ('Rosalind_2391', 'Rosalind_2323'), ('Rosalind_0498', 'Rosalind_0442')]
        self.assertEqual(set(expected), set(actual), msg='{0},{1}'.format(expected, actual))

    def test_compare_base_count_sums(self):
        """
        simplest way only works for simplest examples.
        """
        labeled = parse_nodes(self.data)
        sample = list(compare_multiple(labeled))[0]
        current = sample[0]
        overlaps = sample[1]
        self.assertEqual(compare_base_counts(current, overlaps[0]), 1)
        self.assertEqual(compare_base_counts(current, overlaps[1]), 2)
        self.assertEqual(compare_base_counts(overlaps[0], overlaps[1]), 0)

    def test_compare_base_count_scorelists(self):
        a = ('Rosalind_3894', 'TACGTACCCGTAAGTTCATCTACATGTGTTGCAAAGGAAATATAAAACCCTATTCAAGATTTTTTAATATTCAATCAAATTCTCTCATGGCATGGT')
        b = ('Rosalind_9028', 'TGGGTTCTTTAGGGTGCCGAATGAGTATAAAGTGCCCTCCGACATATTACCAGTTCGGCCATCCGTTTTGTACCTCTTATAGAGACTATTCACGG')
        score_a = compare_base_counts(a,b)
        score_b = compare_base_counts(b,a)
        self.assertEqual(score_a, score_b)

    def test_compare_base_count_scores_equal_lengths(self):
        """
        debugging to make this work better on longer sequences, where totals
        are basically just reporting on sequence similarity, not matches.
        """
        ex1 = ('fake1', 'ATCGTAA')
        ex2 = ('fake2', 'TAAGCAT')
        self.assertEqual(compare_base_counts(ex1, ex2), 2)

    def test_compare_base_count_scores_unequal_lengths(self):
        ex1 = ('fake1', 'ATCGTAA')
        ex2 = ('fake2', 'TAAGCATG')
        self.assertEqual(compare_base_counts(ex1, ex2), 2)

    def test_make_score_dict(self):
        labeled = parse_nodes(self.data)
        sample = list(compare_multiple(labeled))[0]
        current = sample[0]
        overlaps = sample[1]
        scored_pairs = make_score_dict(current, overlaps)
        self.assertNotIn((current, current), scored_pairs.keys())
        self.assertEqual(len(scored_pairs), 2)
        self.assertEqual(sorted(scored_pairs.values()), [1, 2])

    def test_pick_best_matches(self): #note that the current scoring includes identity matches that might be irrelevant
        labeled = parse_nodes(self.data)
        sample = list(compare_multiple(labeled))[0]
        current = sample[0]
        overlaps = sample[1]
        scored_pairs = make_score_dict(current, overlaps)
        best_pair = pick_best_matches(scored_pairs)
        self.assertEqual(best_pair, (('Rosalind_0498', 'AAATAAA'), ('Rosalind_0442', 'AAATCCC')))

    def test_equally_good_matches(self):
        current = ('fake1', 'AAA')
        overlaps = [('fake2', 'AAA'), ('fake3', 'AAA')]
        self.assertGreater(len(overlaps), 1)
        scored_pairs = make_score_dict(current, overlaps)
        best_pair = pick_best_matches(scored_pairs)
        self.assertGreater(len(best_pair), 1)
        self.assertIn(('fake2', 'AAA'), sorted(list(best_pair))[0])
        self.assertIn(('fake3', 'AAA'), sorted(list(best_pair))[1])

    def test_directional_best_pair(self):
        labeled = parse_nodes(self.data)
        sample = list(compare_multiple(labeled))[0]
        current = sample[0]
        overlaps = sample[1]
        scored_pairs = make_score_dict(current, overlaps)
        self.assertNotIn((current, current), scored_pairs.keys())
        best_pair = pick_best_matches(scored_pairs)
        self.assertNotIn((current, current), list(best_pair))
        tup = directional(list(best_pair)[0], list(best_pair)[1])
        self.assertEqual(tup, ('Rosalind_0498', 'Rosalind_0442'))

    def test_directional_multiple(self):
        labeled = parse_nodes(self.data)
        comparer = compare_multiple(labeled)
        current, overlaps = next(comparer)
        path = overlaps.pop(0)
        self.assertEqual(directional(current, path), ('Rosalind_0498', 'Rosalind_2391'))

    def test_old_parser(self):
        parser = parse_data(self.big_data)
        name, sequence = next(parser)
        self.assertEqual(name, 'Rosalind_3496')
        self.assertEqual(sequence,
        'ATGGCAGTCCGAGTTCACGAACCGAATACGTTTAATAGGTAGTCGCCACCACTTAGACGGGTTCTCGCCTATAGGGAACATTAAAGGCGTGGAATTCG')
        self.assertEqual(len(self.big_data), 0)

if __name__=='__main__':
    unittest.main()

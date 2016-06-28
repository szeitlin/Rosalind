__author__ = 'szeitlin'

import unittest
from overlap import overlap, base_counts, directional, parse_nodes, compare_multiple
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
        self.longMessage = True
        labeled = parse_nodes(self.data)
        actual = list(compare_multiple(labeled))[0]
        expected = (('Rosalind_0498', 'AAATAAA'),
         [('Rosalind_2391', 'AAATTTT'), ('Rosalind_0442', 'AAATCCC')])

        self.assertEqual(expected, actual, msg='{0},{1}'.format(expected, actual))

    def test_directional_multiple(self):
        labeled = parse_nodes(self.data)
        comparer = compare_multiple(labeled)
        current, overlaps = next(comparer)
        path = overlaps.pop(0)
        self.assertEqual(directional(current, path), ('Rosalind_0498', 'Rosalind_2391'))

    def test_old_parser(self):
        parser = parse_data(self.big_data)
        name, sequence = next(parser)
        self.assertEqual(name, 'Rosalind_5804')
        self.assertEqual(sequence,
        'ATGGCAGTCCGAGTTCACGAACCGAATACGTTTAATAGGTAGTCGCCACCACTTAGACGGGTTCTCGCCTATAGGGAACATTAAAGGCGTGGAATTCG')

if __name__=='__main__':
    unittest.main()

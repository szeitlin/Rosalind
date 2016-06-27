import unittest
from gc_content import gc_content, parse_data

class TestGCContent(unittest.TestCase):
    def setUp(cls):
        with open('sample_gc_data.txt', 'r') as f:
            cls.data = f.readlines()
        with open('sample_gc_data_4.txt', 'r') as f:
            cls.big_data = f.readlines()

    def test_raw_parsing_one(self):
        self.assertEqual(len(self.data[1].strip() + self.data[2].strip()), 87)
        name, sequence = parse_data(self.data)
        self.assertEqual(name, 'Rosalind_0808')
        self.assertEqual(len(sequence), 87)

    def test_gc_content(self):
        name, sequence = parse_data(self.data)
        name, percent = gc_content(name, sequence, debug=True)
        self.assertEqual(percent, 60.919540)

    def test_multiple_sequences(self):
        name, sequence = parse_data(self.big_data)
        self.assertEqual(name, 'Rosalind_0808')
        name, percent = gc_content(name, sequence, debug=True)
        self.assertEqual(percent, 60.919540)

if __name__=='__main__':
    unittest.main()


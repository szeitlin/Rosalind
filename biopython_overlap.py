__author__ = 'szeitlin'

from Bio import SeqIO

def get_records(filename):
    """
    :param filename: fasta format file
    :return: list of sequence record objects with names
    """
    filename = "rosalind_grph.txt"
    records = (r for r in SeqIO.parse(filename, "fasta"))

    return records


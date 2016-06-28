__author__ = 'szeitlin'

from gc_content import parse_data

def overlap(one, two):
    """
    Test whether two sequences share similar motifs on the ends, i.e.
    one has it as a suffix, and the other has it as a prefix.

    Note that this doesn't do anything about returning results in order.

    :param one: str
    :param two: str
    :return: bool

    >>> overlap("AAATAAA", "AAATTTT")
    True
    >>> overlap("AAATTTT", "TTTTCCC")
    True
    >>> overlap("AAATAAA", "TTTTCCC")
    False
    >>> overlap("AAATTAA", "AAATTTT")
    False
    """
    counts1 = base_counts(one)
    counts2 = base_counts(two)

    if counts1 == counts2:
        return False

    elif (counts1[0] == counts2[-1]) or (counts1[-1] == counts2[0]):
        return True

    else:
        return False

def directional(one, two):
    """
    Return overlapping sequences in the right order.

    :param one: tuple of (str, str) where the first str is the name, second is seq
    :param two: tuple of (str, str) ""
    :return: names in the correct order

    >>> directional(('Rosalind_2391', 'AAATTTT'), ('Rosalind_0498', 'AAATAAA'))
    ['Rosalind_0498', 'Rosalind_2391']
    """
    counts1 = base_counts(one[1])
    counts2 = base_counts(two[1])

    if (counts1[0] == counts2[-1]):
        return two[0], one[0]
    elif (counts1[-1] == counts2[0]):
        return one[0], two[0]

def base_counts(seq):
    """
    Reduce a string to counts of characters.
    :param seq: str
    :return: list of str of format char+int

    >>> base_counts("ATCG")
    ['A1', 'T1', 'C1', 'G1']
    >>> base_counts("AAATAAAA")
    ['A3', 'T1', 'A4']
    >>> base_counts("AAATTTT")
    ['A3', 'T4']
    >>> base_counts("TTTTCCC")
    ['T4', 'C3']

    """
    tmp = seq[0]
    ls = []
    count = 1

    for char in seq[1:]:
        if char != tmp:
            ls.append(tmp+str(count))
            tmp = char
            count = 1
        elif char == tmp:
            count += 1

    ls.append(tmp+str(count))

    return ls

def base_totals(seq):
    """
    Count total numbers of bases in seq.
    :param seq: str
    :return: dict of char:count(int)

    >>> base_totals("ATCG")
    {'A':1, 'T':1, 'C':1, 'G':1}
    >>> base_totals("AAATAAA")
    {'A':6, 'T':1}

    """
    totals = dict()
    for char in seq:
        if char not in totals:
            totals.update({char:1})
        elif char in totals:
            totals[char] +=1

    return totals

def compare_multiple(labeled):
    """
    Find overlaps across more than pairs of sequences.

    :param listofseq: list of tuples of (str, str) with name, seq
    :return: list of names that overlap

    >>> compare_multiple([('Rosalind_0498', 'AAATAAA'), ('Rosalind_2391', 'AAATTTT'),\
    ('Rosalind_2323', 'TTTTCCC'), ('Rosalind_0442', 'AAATCCC'), ('Rosalind_5013', 'GGGTGGG')])
    ('Rosalind_0498', 'AAATAAA'), [('Rosalind_2391', 'AAATTTT'), ('Rosalind_0442', 'AAATCCC')]

    """
    while labeled:
        current = labeled.pop(0)
        compare = [overlap(current[1], x[1]) for x in labeled]
        compared = [(x,y) for (x,y) in zip(labeled, compare)]
        overlaps = [x[0] for x in compared if x[1] is True]

        yield current, overlaps

def parse_nodes(data):
    """
    For testing only.
    Clean up and pair names with sequences.

    :param data: list of lines from text file
    :return: paired tuples of (str, str) with name, seq
    """

    names = [x[1:].strip() for x in data[::2]]
    listofseq = [x.strip() for x in data[1::2]]
    labeled = [(x,y) for (x,y) in zip(names, listofseq)]

    return labeled


if __name__=='__main__':
    # import doctest
    # doctest.testmod()

    with open('rosalind_grph.txt', 'r') as f:
        data = f.readlines()

    labeled = list(parse_data(data))
    comparer = compare_multiple(labeled)
    printer = lambda tup: print('{} {}'.format(tup[0],tup[1]))

    while comparer:
        try:
            current, overlaps = next(comparer)
            while len(overlaps) > 1:
                path = overlaps.pop()
                tup = directional(current, path)
                printer(tup)
            else:
                if len(overlaps) == 1:
                    tup = directional(current, overlaps[0])
                    printer(tup)

        except StopIteration:
            break

#have to do something to remove duplicates/break ties

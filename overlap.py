__author__ = 'szeitlin'

import operator
from gc_content import parse_data

def overlap(counts1, counts2):
    """
    Simplest test for whether two sequences share similar motifs on the ends, i.e.
    one has it as a suffix, and the other has it as a prefix.

    Note that this doesn't do anything about returning results in order.

    :param one: base counts for a str
    :param two: base counts for a str
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

def compare_base_counts(one, two):
    """
    Get the base_counts and use it to score the overlap for two str.
    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: score (int)
    """
    counts1, counts2 = get_base_counts(one, two)

    #for now, try just using a 1 if there's a match, 0 if not, and sum that.
    scorelist = []

    #have to reverse one b/c we want overlap, not identity
    #if they're not the same length, always reverse the longer one b/c zip will truncate

    #avoid calculating the length repeatedly, b/c it's slow
    one_len = len(counts1)
    two_len = len(counts2)

    if (one_len == two_len) or (two_len > one_len):
        original = counts1
        flipped = reversed(counts2)
    elif one_len > two_len:
        original = counts2
        flipped = reversed(counts1)

    for x,y in zip(original, flipped):
        if x==y:
            scorelist.append(1)
        else:
            scorelist.append(0)

    return sum(scorelist)

def get_base_counts(one, two):
    """
    Applies the base_counts method to two strings and saves the results to variables for re-use.
    :param one: tuple of (str, str) with name, seq
    :param two: tuple of (str, str) with name, seq
    :return: two lists of str (of format char + int)
    >>> base_counts("ATCG")
    ['A1', 'T1', 'C1', 'G1']
    """
    counts1 = base_counts(one[1])
    counts2 = base_counts(two[1])

    return counts1, counts2

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
    :return: tuple of current (tuple of str,str) and overlaps (list of tuples of str,str)

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

def make_score_dict(current, overlaps):
    """
    Score multiple overlaps for ranking best matches.

    :param current: tuple of (str,str) with name, seq
    :param overlaps: list of tuples of (str,str) with name, seq
    :return:
    """
    scored_pairs = dict()

    while len(overlaps) > 1:
        mate = overlaps.pop(0)
        #score them by how well they match
        score = compare_base_counts(current, mate)
        scored_pairs[current, mate] = score

    #get the last one
    mate = overlaps[0]
    score = compare_base_counts(current, mate)
    scored_pairs[current, mate] = score

    return scored_pairs

def pick_best_matches(scored_pairs):
    """
    If scored_pairs have different scores, return the highest one.
    If the scores are the same, return multiple values.

    :param scored_pairs: dict of
    (str,str) tuple keys with (name, seq) pairs: score (int) values
    :return: list of keys with the best scores
    """
    #if all values are equal, return all the keys
    if len(set(scored_pairs.values())) == 1:
        return scored_pairs.keys()

    #otherwise, return the highest one
    elif len(set(scored_pairs.values())) > 1:
        return sorted(scored_pairs.items(), key=operator.itemgetter(1))[-1][0]

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

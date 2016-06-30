__author__ = 'szeitlin'

import operator

def longest_overlap(counts1, counts2):
    """
    Helper for compare_base_counts. Compares compressed base count lists in both
    orientations (1,2 and 2,1)

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: count (int) of maximum number of overlapping bases at the ends


    >>> longest_overlap(['A1', 'T1'], ['T1', 'C1'])
    1
    >>> longest_overlap(['A3', 'T1', 'A4'], ['T1', 'A4', 'T1', 'C3'])
    2
    >>> longest_overlap(['A4', 'G2', 'A1', 'C4'], ['T4', 'C3', 'A4', 'G2', 'A1'])
    3
    >>> longest_overlap(['G3', 'T3'], ['A3', 'G3'])
    1
    """

    lengths = {tuple(counts1): len(counts1), tuple(counts2): len(counts2)}

    shorter, longer = [x[0] for x in sorted(lengths.items(), key=operator.itemgetter(1))]

    shorter_index = [-x for x in range(1, lengths[shorter]+1)]
    longer_index = [x for x in range(lengths[longer])]

    scores = dict()

    for i in shorter_index:
        scores[i] = []

        for j in longer_index:
            if shorter[i] != longer[j]:
                count = 0
            elif shorter[i] == longer[j]:
                count = 1
                scores[i].append(count)

    #print(scores)

    #forward: sum by sequential j
    forward = max([sum(x) for x in scores.values()])

    #reverse: sum by sequential i
    ordered = sorted(scores.items())
    total = 0
    for x,y in ordered:
        if len(y) > 0:
            total += sum(y)
        elif len(y) == 0:
            break
    reverse = total

    return max(forward, reverse)


if __name__=='__main__':
    import doctest
    doctest.testmod()


__author__ = 'szeitlin'

import operator

def longest_overlap(counts1, counts2):
    """
    Helper for compare_base_counts. Compares compressed base count lists.

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: count (int) of maximum number of overlapping bases at the ends

    >>> longest_overlap(['A1', 'T1'], ['T1', 'C1'])
    1
    >>> longest_overlap(['A3', 'T1', 'A4'], ['T1', 'A4', 'T1', 'C3'])
    2
    >>> longest_overlap(['T4', 'C3', 'A4', 'G2', 'A1'], ['A4', 'G2', 'A1', 'C4'])
    3
    >>> longest_overlap(['G3', 'T3'], ['A3', 'G3'])
    1
    """
    #this is silly, could use the length as the key and skip the fancy sorting

    lengths = {tuple(counts1): len(counts1), tuple(counts2): len(counts2)}

    shorter, longer = [x[0] for x in sorted(lengths.items(), key=operator.itemgetter(1))]

    i = -1
    tmp = shorter[i]
    scorelist = []
    count = 1

    for j in range(lengths[longer]):
        if longer[j] != tmp:
            count = 0 #not necessary, just noting for clarity
            if i != -(lengths[shorter]):
                i -= 1
                tmp = shorter[i]
            else:
                print("at i {} got {}".format(i, scorelist))

        elif longer[j] == tmp: #keep going without shifting
            count = 1
            scorelist.append(count)
            while i != -1:
                i +=1
                if longer[j] != shorter[i]:
                    count = 0
                elif longer[j] == shorter[i]:
                    count = 1
                    scorelist.append(count)
            else:
                print("at i {} got {}".format(i, scorelist))

    scorelist.append(count)

    return scorelist


if __name__=='__main__':
    import doctest
    doctest.testmod()


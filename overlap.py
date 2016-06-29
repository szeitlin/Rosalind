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

    print(counts1, counts2)

    if (counts1[0] == counts2[-1]):
        return two[0], one[0]
    elif (counts1[-1] == counts2[0]) or (counts1 == counts2):
        return one[0], two[0]
    else:
        raise Exception("possible overlap error here")

def compare_base_counts(one, two):
    """
    Get the base_counts and use it to score the maximum end overlap for two str.
    Allow mismatch followed by match,
    don't allow match followed by mismatch.

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: score (int)
    """
    counts1, counts2 = get_base_counts(one, two)

    #NOTE: we want overlap, not identity and not complementarity

    #avoid calculating the length repeatedly, b/c it's slow
    one_len = len(counts1)
    two_len = len(counts2)

    i = -1
    scorelist = []

    for j in range(min(one_len, two_len)):
        if counts1[i] != counts2[j]:
            if any([x > 0 for x in scorelist]):
                break
            else:
                #penalty for mismatches, otherwise just get similarity
                scorelist.append(-1)

        elif counts1[i] == counts2[j]:
            scorelist.append(1)

    return sum(scorelist)

def get_o3_overlap_only(one, two):
    """
    Instead of using base_counts to get maximum overlap,
    just score the overlap of the 3 end bases.

    :param one: tuple of name, seq
    :param two: tuple of name, seq
    :return: overlap score (int)
    """
    i = -1
    scorelist = []

    one_len = len(one[1])
    two_len = len(two[1])

    for j in range(3):
        if one[1][i] != two[1][j]:
            if any([x > 0 for x in scorelist]):
                break
            else:
                #penalty for mismatches, otherwise just get similarity
                scorelist.append(-1)

        elif one[1][i] == two[1][j]:
            scorelist.append(1)

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

def compare_multiple(labeled, debug=False, unlimited=False):
    """
    Find overlaps across more than pairs of sequences.

    unlimited option will get maximum overlap.
    otherwise default looks at overlap of only 3 bases.

    :param listofseq: list of tuples of (str, str) with name, seq
    :return: tuple of best match

    >>> compare_multiple([('Rosalind_0498', 'AAATAAA'), ('Rosalind_2391', 'AAATTTT'),\
    ('Rosalind_2323', 'TTTTCCC'), ('Rosalind_0442', 'AAATCCC'), ('Rosalind_5013', 'GGGTGGG')])
    ('Rosalind_0498', 'AAATAAA'), [('Rosalind_2391', 'AAATTTT'), ('Rosalind_0442', 'AAATCCC')]

    """
    score_dict = dict()

    while len(labeled) >=2:

        current = labeled.pop(0)
        #print("current is {}".format(current))

        for i in range(len(labeled)):
         #   print(score_dict)
            x = labeled[i]
         #   print("comparing to {}".format(x))

            if unlimited == True:
                score1 = compare_base_counts(current, x)
                score2 = compare_base_counts(x, current)
            else:
                score1 = get_o3_overlap_only(current, x)
                score2 = get_o3_overlap_only(x, current)

         #   print(current, x, score1)
         #   print(x, current, score2)

            lookup = current[0]

            if score1 == score2:
                if score1 <= 0:
                    continue

            if any(lookup in x for x in score_dict.keys()):
                oldmatch = [x for x in score_dict.keys() if lookup in x]
                oldscore = score_dict[oldmatch[0]]
          #      print("found an existing score {}: {}".format(oldmatch, oldscore))

                if (oldscore > score1) and (oldscore > score2):
                    continue

                elif oldscore:
                    #if new scores are equal and better (unlikely)
                    if (score1 == score2) and (score1 > oldscore):
                       # print("equal and better!")
                        del score_dict[oldmatch[0]] #remove the old match if it's lower
                        score_dict[(lookup, x[0])] = score1

                    #if new scores are unequal
                    elif (score1 > oldscore) or (score2 > oldscore):
                       # print("one new score is better!")
                        del score_dict[oldmatch[0]]
                        if score1 > oldscore:
                            score_dict[(lookup, x[0])] = score1
                        elif score2 > oldscore:
                            score_dict[(x[0], lookup)] = score2

                    #don't delete them if they're at least as good
                    elif (score1 == oldscore) or (score2 == oldscore):
                       # print("scores are at least as good as before!")
                        if score1 == oldscore:
                            score_dict[(lookup, x[0])] = score1
                        elif score2 == oldscore:
                            score_dict[(x[0], lookup)] = score2

            elif (score1 > score2) and (score1 > 0):
                score_dict[(lookup, x[0])] = score1
            elif (score1 < score2) and (score2 > 0):
                score_dict[(x[0], lookup)] = score2

    if debug==True:
        return score_dict
    else:
        return list(score_dict.keys())

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
    :return: tuple of tuples with the best scores
    """
    #if all values are equal, return all the keys
    if len(set(scored_pairs.values())) == 1:
        return list(scored_pairs.keys())

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
    scored = compare_multiple(labeled, debug=True)
    print(scored)

    #to make a graph with Gephi:
    # with open("overlaps.csv", 'w') as results:
    #     for item in scored:
    #         results.write("{};{}\n".format(item[0], item[1]))




def find_motif(sequence, motif):
    """
    given a sequence(str) and motif(str)
    return the positions (1-indexed) of each occurrence of the motif
    >>> find_motif("GATATATGCATATACTT", "ATAT")
    2 4 10
    """
    indices = [(i, len(sequence)) for i in reversed(range(len(sequence)))]
    #print(indices)

    matches = []

    for tup in indices:
        if (tup[1] - tup[0]) >= len(motif):
            if motif in sequence[tup[0]:tup[1]+1]:
                #print(sequence[tup[0]:tup[1]+1])

                match = sequence[tup[0]:tup[1]+1].find(motif)
                matches.append(tup[0] + match) #convert back to where they are in the whole seq
        
    one_indexed = sorted([x+1 for x in set(matches)])
    #print(one_indexed)

    printable = " ".join([str(x) for x in one_indexed])
    print(printable)

if __name__=='__main__':
#   import doctest
#   doctest.testmod()
    
    with open('rosalind_subs.txt', 'r') as f:
        data = f.readlines()
        sequence = data[0].strip()
        motif = data[1].strip()
        find_motif(sequence, motif)



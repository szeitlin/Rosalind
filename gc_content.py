def gc_content(name, sequence, debug=False):
    """
    Calculates the percentage of GC bases in a FASTA format sequence.
    returns the unique id and the percentage. 
    input file contains at most 10 DNA strings of length max 1 kb each. 

    >>> gc_content(sample_dataset)
    Rosalind_0808
    60.919540

    """
    total = 0
    gc = 0

    for char in sequence:
        total +=1
        if char in ['G', 'C']:
            gc+=1
                   
    percent = gc/total * 100

    if debug==True:
        return name, percent
    
    else:
        print(name)
        print(percent)



def parse_data(data):
    """ helper to split data into names and sequences."""
    
    name = None
    newstring = ""

    while data:
        line = data.pop(0)

        if line[0] == '>' and name is None:
            name = line[1:].strip()
            newstring = ""

        elif '>' not in line:
            newstring += line.strip()

        elif line[0] == '>' and name is not None:
            yield name, newstring
            name = line[1:].strip()
            newstring = ""

    yield name, newstring
                
     
if __name__=='__main__':
    with open('rosalind_gc.txt', 'r') as f:
        data = f.readlines()

        parser = parse_data(data)
        while parser:
            try:
                name, sequence = next(parser)
                #print(name, sequence)
                name, percent = gc_content(name, sequence, debug=True)
                print(name)
                print(percent)

            except StopIteration:
                break



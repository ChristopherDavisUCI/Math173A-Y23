import string

from collections import Counter

letterset = frozenset(string.ascii_letters)

# From Hoffstein, Pipher, Silverman
english_freq = [0.082, 0.014, 0.028, 0.038, 0.131, 0.029, 0.02, 0.053, 0.064, 0.001, 0.004, 0.034, 0.025, 0.071, 0.08, 0.02, 0.001, 0.068, 0.061, 0.105, 0.025, 0.009, 0.015, 0.002, 0.02, 0.001]

# From Hoffstein, Pipher, Silverman, together with frequency per 1000 words
bigramfreq = [('th',168), ('he',132), ('an',92), ('re',91), ('er',88), ('in',86), ('on',71), ('at',68), ('nd',61), ('st',53), ('es',52), ('en',51), ('of',49), ('te',46), ('ed',46)]

#trigramfreq is based on data from http://www.cryptograms.org/letter-frequencies.php
trigramfreq = ['the', 'and', 'tha', 'ent', 'ing', 'ion', 'tio', 'for', 'nde', 'has', 'nce', 'edt', 'tis', 'oft', 'sth', 'men']

def only_letters(X, case=None):
    X = ''.join(c for c in X if c in letterset)

    if len(X) == 0:
        return None
    
    if case is None:
        return X
    elif case == "lower":
        return X.lower()
    elif case == "upper":
        return X.upper()
    
def count_substrings(X,n):
    if not X:
        return {}
    X = only_letters(X)
    shifts = [X[i:] for i in range(n)]
    grams = [''.join(chrs) for chrs in zip(*shifts)]
    return Counter(grams)
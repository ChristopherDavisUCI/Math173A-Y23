import string
import textwrap
import re
from collections import Counter
from itertools import combinations
import numpy as np

english_freq = {
    'a': 0.0803,
    'b': 0.014,
    'c': 0.0232,
    'd': 0.0467,
    'e': 0.1247,
    'f': 0.0226,
    'g': 0.0209,
    'h': 0.065,
    'i': 0.0683,
    'j': 0.0012,
    'k': 0.008,
    'l': 0.0367,
    'm': 0.0255,
    'n': 0.0706,
    'o': 0.0776,
    'p': 0.0166,
    'q': 0.0011,
    'r': 0.0621,
    's': 0.0626,
    't': 0.0902,
    'u': 0.0279,
    'v': 0.0087,
    'w': 0.0236,
    'x': 0.0012,
    'y': 0.0203,
    'z': 0.0004
}


def only_letters(X, case=None):
    '''Returns the string obtained from X by removing everything but the letters.
    If case="upper" or case="lower", then the letters are all
    converted to the same case.'''
    X = ''.join(c for c in X if c in string.ascii_letters)

    if len(X) == 0:
        return None
    
    if case is None:
        return X
    elif case == "lower":
        return X.lower()
    elif case == "upper":
        return X.upper()


def string_for_code_block(X, linewidth=60):
    return '\n'.join(textwrap.wrap(X, width=linewidth))

    
def add_spaces(X, width=5, linewidth=60):
    one_line = ' '.join(textwrap.wrap(X, width=width))
    many_lines = string_for_code_block(one_line, linewidth=linewidth)
    return many_lines
    

def shift_char(ch, shift_amt):
    '''Shifts a specific character by shift_amt.
    Example:
    shift_char("Y", 3) returns "B"
    '''
    if ch in string.ascii_lowercase:
        base = 'a'
    elif ch in string.ascii_uppercase:
        base = 'A'
    # It's not clear what shifting should mean in other cases
    # so if the character is not upper or lower-case, we leave it unchanged
    else:
        return ch
    return chr((ord(ch)-ord(base)+shift_amt)%26+ord(base))


def shift_string(X, shift_amt):
    '''Shifts all characters in X by the same amount.'''
    return ''.join(shift_char(ch, shift_amt) for ch in X)


def mut_ind_co(d1, d2):
    '''For letter frequency dictionaries d1 and d2, return the Mutual Index of Coincidence.
    See Equation (5.9) on page 222 in Hoffstein, Pipher, Silverman.'''
    s = 0
    for k in d1.keys():
        s += d1.get(k, 0)*d2.get(k,0)
    return s


def ind_co(X):
    X = only_letters(X, case="upper")
    ctr = count_substrings(X, 1)
    n = sum(ctr.values())
    return (1/(n*(n-1)))*sum(f*(f-1) for f in ctr.values())


def weave(string_list):
    output = ''.join([''.join(tup) for tup in zip(*string_list)])
    # The rest is just to deal with the case of unequal string lengths
    # We assume the only possibility is that the early strings are one character longer
    last_length = len(string_list[-1])
    extra = [s[-1] for s in string_list if len(s) > last_length]
    return output + ''.join(extra)


def count_substrings(X,n):
    '''Returns a Python Counter object of all n-grams in X.'''
    if not X:
        return {}
    X = only_letters(X)
    shifts = [X[i:] for i in range(n)]
    grams = [''.join(chrs) for chrs in zip(*shifts)]
    return Counter(grams)


def get_freq(X, case="lower"):
    '''Returns the proportion that each letter occurs in "X"'''
    
    if case == "lower":
        letters = string.ascii_lowercase
    elif case == "upper":
        letters = string.ascii_uppercase
    else:
        raise ValueError("case should be 'upper' or 'lower'.")
    
    X = only_letters(X, case=case)
    n = len(X)
    ctr = count_substrings(X, 1)
    output = {}
    for char in letters:
        output[char] = ctr[char]/n
    return output


def kasiski_diffs(Y, case="upper"):
    Y = only_letters(Y, case=case)
    ctr = count_substrings(Y, 3)
    tri_reps = [k for k,v in ctr.items() if v > 1]
    diffs = []
    for tri in tri_reps:
       starts = [m.start() for m in re.finditer(f'(?={tri})', Y)]
       diffs.extend([abs(x-y) for x,y in combinations(starts, 2)])
 
    return np.array(sorted(diffs))
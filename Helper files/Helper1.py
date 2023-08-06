import string
from collections import Counter

import numpy as np
import pandas as pd
import altair as alt

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


def get_shift_ciphertext(source, length):
    source = only_letters(source, case="upper")
    rng = np.random.default_rng()
    start = rng.integers(0, len(source) - length + 1)
    plaintext = source[start: start+length]
    shift_amt = rng.integers(1, 26)
    return shift_string(plaintext, shift_amt)


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


def freq_chart(X, case="upper"):
    '''Plot the letter frequency chart.'''
    X = only_letters(X, case=case)
    if case == "lower":
        letters = list(string.ascii_lowercase)
    elif case == "upper":
        letters = list(string.ascii_uppercase)
    else:
        raise ValueError("case should be 'upper' or 'lower'.")

    freq_dict = get_freq(X, case=case)
    ser_count = pd.Series(freq_dict, name="freq")
    df_count = pd.DataFrame(ser_count).reset_index()
    df_count.rename({"index": "letter"}, axis=1, inplace=True)

    chart = alt.Chart(df_count).mark_bar().encode(
        x=alt.X("letter", scale=alt.Scale(domain=letters)),
        y="freq",
        tooltip=["letter", "freq"]
    )

    return chart


def mut_ind_co(d1, d2):
    '''For letter frequency dictionaries d1 and d2, return the Mutual Index of Coincidence.
    See Equation (5.9) on page 222 in Hoffstein, Pipher, Silverman.'''
    s = 0
    for k in d1.keys():
        s += d1.get(k, 0)*d2.get(k,0)
    return s


def ind_co(d):
    '''Return an estimate for the index of coincidence for the letter frequency dictionary d.
    Note: We are computing the probability of drawing the same letter twice "with replacement".
    The precise definition is "without replacement".'''
    return mut_ind_co(d, d)
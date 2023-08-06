import string
import textwrap

def string_for_code_block(X, linewidth=60):
    return '\n'.join(textwrap.wrap(X, width=linewidth))

    
def add_spaces(X, width=5, linewidth=60):
    one_line = ' '.join(textwrap.wrap(X, width=width))
    many_lines = string_for_code_block(one_line, linewidth=linewidth)
    return many_lines


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


def weave(string_list):
    output = ''.join([''.join(tup) for tup in zip(*string_list)])
    # The rest is just to deal with the case of unequal string lengths
    # We assume the only possibility is that the early strings are one character longer
    last_length = len(string_list[-1])
    extra = [s[-1] for s in string_list if len(s) > last_length]
    return output + ''.join(extra)


def to_base_b(num, base):
    '''Returns the digits of `num` when written in base `base`.
    Adapted from code on Stack Overflow.'''
    digits = []
    while num > 0:
        num, rem = divmod(num, base)
        digits.append(rem)
    return digits[::-1]


def from_base_b(digit_list, base):
    '''Converts from a list of digits in base `base` to an integer.'''
    return sum(d*base**i for i, d in enumerate(digit_list[::-1]))


def factor_out_2(num):
    '''Returns (k, q) such that num equals 2^k * q'''
    if (not isinstance(num, int)) or (num <= 0):
        raise ValueError("The input should be a positive integer.")
    q,r = divmod(num, 2)
    v = 0
    while r == 0:
        v += 1
        num = q
        q, r = divmod(q, 2)
    return (v, num)
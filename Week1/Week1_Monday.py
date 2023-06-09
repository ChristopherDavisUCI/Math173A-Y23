import streamlit as st
import string
import textwrap
import numpy as np
import pandas as pd
import altair as alt

letterset = frozenset(string.ascii_letters)

englishfreq = [0.082, 0.014, 0.028, 0.038, 0.131, 0.029, 0.02, 0.053, 0.064, 0.001, 0.004, 0.034, 0.025, 0.071, 0.08, 0.02, 0.001, 0.068, 0.061, 0.105, 0.025, 0.009, 0.015, 0.002, 0.02, 0.001]

df_english_freq = pd.DataFrame({"freq": englishfreq, "letter": list(string.ascii_lowercase)})

freq_chart = alt.Chart(df_english_freq).mark_bar().encode(
    x="letter",
    y="freq",
    tooltip="freq"
)

rng = np.random.default_rng()

def only_letters(X, case=None):
    X = ''.join(filter(letterset.__contains__, X))

    if len(X) == 0:
        return None
    
    if case is None:
        return X
    elif case == "lower":
        return X.lower()
    elif case == "upper":
        return X.upper()
    
def string_for_code_block(X, linewidth=50):
    return '\n'.join(textwrap.wrap(X, width=linewidth))
    
def add_spaces(X, width=5, linewidth=50):
    one_line = ' '.join(textwrap.wrap(X, width=width))
    many_lines = string_for_code_block(one_line, linewidth=linewidth)
    return many_lines

def countsubstrings(X,n):
    if not X:
        return {}
    X = only_letters(X)
    subdict = {}
    for i in range(0,len(X)-n+1):
        if X[i:i+n] in subdict:
            subdict[X[i:i+n]] += 1
        else:
            subdict[X[i:i+n]] = 1
    return subdict

def shift_encrypt(X=None, shift_amt = None, spaces=False, key=None):
    if not X:
        if key and key in st.session_state:
            st.session_state[key] = ""
        return None
    
    X = only_letters(X, case="upper")

    if len(X) == 0:
        return None
    
    if shift_amt is None:
        shift_amt = rng.integers(1,26)

    X = ''.join(chr((ord(ch)-ord('A')+shift_amt)%26+ord('A')) for ch in X)

    if spaces:
        X = add_spaces(X)

    if key:
        st.session_state[key] = X

    return X

st.title("The Shift Cipher")

st.markdown("""Paste a block of plaintext below and click the `encrypt` button.  The text will be shift encrypted using a secret key.  Can you use cryptanalysis to find the secret shift amount?""")

plaintext = st.text_area(label="Your plaintext here")

enc_button = st.button(
                        "Encrypt",
                        on_click=shift_encrypt, 
                        kwargs={"X": plaintext, "shift_amt": None, "spaces": True, "key": "ciphertext"}
                    )

try:
    st.code(st.session_state["ciphertext"])
except KeyError:
    disp = '''Click the above button to encrypt your plaintext using the shift cipher with a randomly chosen shift amount.'''
    st.text_area(label="Placeholder", value=disp)

st.header("Letter frequencies")

st.write("Here is the expected letter frequency in English:")

st.altair_chart(freq_chart, use_container_width=True)

shift_amt = st.slider("Shift amount", min_value=-50, max_value=50, value=0, step=1)

st.write("Here are the letter counts in the shifted ciphertext:")

try:
    subdict = countsubstrings(shift_encrypt(st.session_state["ciphertext"], shift_amt, spaces=False), 1)
    ser_count = pd.Series(subdict, name="count")
    df_count = pd.DataFrame(ser_count).reset_index()
    df_count.rename({"index": "letter"}, axis=1, inplace=True)

    cipher_chart = alt.Chart(df_count).mark_bar().encode(
        x=alt.X("letter", scale=alt.Scale(domain=list(string.ascii_uppercase))),
        y="count",
        tooltip="count"
    )

    st.altair_chart(cipher_chart, use_container_width=True)
except KeyError:
    pass

st.header("Index of coincidence")

st.write("For the listed shift amounts, we state the index of coincidence.")

try:
    subdict = countsubstrings(st.session_state["ciphertext"], 1)
    freqs = np.array([subdict.get(c,0) for c in string.ascii_uppercase])
    freqs = list(freqs/freqs.sum())
    coins = {}
    for i in range(-25, 26):
        j = i%26
        # Think about why we need the -j here
        coins[i] = np.dot(englishfreq, freqs[-j:]+freqs[:-j])
    ser = pd.Series(coins, name="score")
    df_score = pd.DataFrame(ser).reset_index()
    df_score.rename({"index": "shift_amount"}, axis=1, inplace=True)
    c = alt.Chart(df_score).mark_bar().encode(
        x="shift_amount:O",
        y="score",
        color = alt.condition(
            alt.datum.score > 0.06,
            alt.value("orange"),
            alt.value("steelblue")
        ),
        tooltip = ["shift_amount", "score"]
    )
    st.altair_chart(c, use_container_width=True)
except (KeyError, ValueError):
    pass

st.header("Decryption")

st.write("Once we think we know the shift amount, we can attempt to decrypt the ciphertext.")

decrypt_amt = st.slider("Shift for decryption", min_value=-50, max_value=50, value=0, step=1)

try:
    X = shift_encrypt(st.session_state["ciphertext"], decrypt_amt, spaces=False)
    X_newline = string_for_code_block(X)
    st.code(X_newline)
except KeyError:
    pass

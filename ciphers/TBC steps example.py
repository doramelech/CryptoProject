from streamlit_extras.steps import *
import streamlit as st
from ciphers.time_based_cipher import (
    _affine_encrypt,
    _myszkowski_encrypt,
    _two_square_encrypt,
    GetTime,
    WORDS,
    _extract_special_chars,
    _restore_special_chars
)


def _word_from_number(number):
    return WORDS[(number - 1) % len(WORDS)]

def TBCExample():
    s = steps(
        ["Text to Encrypt", "Affine", "Two Square Cipher", "Myszkowski Cipher"],
        key="steps",
    )
    with s[0]:
        if "gotoprevious" not in st.session_state:
            st.session_state.gotoprevious = False
        if "current_time" not in st.session_state:
            st.session_state.current_time = GetTime()
        if "source_text" not in st.session_state:
            st.session_state.source_text = ""
        if "affine_text" not in st.session_state:
            st.session_state.affine_text = ""
        if "square_text" not in st.session_state:
            st.session_state.square_text = ""
        if "final_text" not in st.session_state:
            st.session_state.final_text = ""
        if "special_chars_info" not in st.session_state:
            st.session_state.special_chars_info = []


        time = st.session_state.current_time
        
        st.write(
            f"The time now is  M{time['month']:02d} D{time['day']:02d}"
            f" {time['hour']:02d}:{time['minute']:02d}:{time['second']:02d}"
            f" \n we'll use this time for our example"
        )
        prompt = "enter a text you want to encrypt"
        if st.session_state.gotoprevious:
            prompt = "you need to enter a text before advancing..."
        st.session_state.source_text = st.text_input(
            prompt,
            value=st.session_state.source_text,
            key="example_text_input",
        )
        st.session_state.special_chars_info = _extract_special_chars(st.session_state.source_text)

        if st.button("Next", key="steps_next_0"):
            if st.session_state.source_text.strip():
                st.session_state.gotoprevious = False
                s.next()
            else:
                st.session_state.gotoprevious = True

    with s[1]:
        if not st.session_state.source_text.strip():
            st.warning("Please enter some text on the first step.")
            return

        st.write("to start - we'll use the minutes and the hours as the a, b keys of our affine cipher."
                 f"\n so our text turns from"
                 f"\n {_restore_special_chars(st.session_state.source_text, st.session_state.special_chars_info[1])}"
                 f"\n to... \n ")
        st.session_state.affine_text = _affine_encrypt(
            st.session_state.source_text,
            st.session_state.current_time["minute"],
            st.session_state.current_time["hour"],
        )
        st.write(_restore_special_chars(st.session_state.affine_text, st.session_state.special_chars_info[1]))

        if st.button("Next", key="steps_next_1"):
            s.next()

    with s[2]:

        st.write("Next, we'll take the month and the day and take the words in the \n index of those months as the two key words of our two square cipher\n "
                 f"so {_restore_special_chars(st.session_state.affine_text, st.session_state.special_chars_info[1])} will turn into")
        month_word = _word_from_number(st.session_state.current_time["month"])
        day_word = _word_from_number(st.session_state.current_time["day"])
        st.session_state.square_text = _two_square_encrypt(
            st.session_state.affine_text,
            month_word,
            day_word,
        )
        st.write(_restore_special_chars(st.session_state.square_text, st.session_state.special_chars_info[1]))
        if st.button("Next", key="steps_next_2"):
            s.next()

    with s[3]:

        st.write("Lastly, we'll use a Myszkowski cipher and our key will be the seconds: \n"
                 f"{_restore_special_chars(st.session_state.square_text, st.session_state.special_chars_info[1])}")
        st.session_state.final_text = _myszkowski_encrypt(
            st.session_state.square_text,
            st.session_state.current_time["second"],
        )
        st.write(_restore_special_chars(st.session_state.final_text, st.session_state.special_chars_info[1]))


        if st.button("Reset", key="steps_reset"):
            s.reset()
            st.session_state.source_text = ""
            st.session_state.affine_text = ""
            st.session_state.square_text = ""
            st.session_state.final_text = ""
            st.session_state.gotoprevious = False

TBCExample()

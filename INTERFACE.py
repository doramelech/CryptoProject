import streamlit as st
from time_based_cipher import TBC
from yonch_cipher import YonchCipher

def general_cipher(text, cipher, mode, time_value=None ):
    try:
        if cipher == "TBC":
            return TBC(text, time_value, mode)
        return YonchCipher(text, mode)
    except Exception as e:
        return e




import json
import hashlib
import hmac
from pathlib import Path

import streamlit as st
from time_based_cipher import TBC, GetTime
from yonch_cipher import YonchCipher

def general_cipher(text, cipher, mode, time_value=None ):
    try:
        if cipher == "TBC":
            if time_value is None:
                time_value = GetTime()
            return TBC(text, time_value, mode)
        return YonchCipher(text, mode)
    except Exception as e:
        return e




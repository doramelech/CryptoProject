import importlib
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ciphers.time_based_cipher import TBC, GetTime
from ciphers.tbc_hack import *
from ciphers.yonch_cipher import YonchCipher
from INTERFACE import *

def test_tbc_round_trip():
    time_value = {
        "month": 5,
        "day": 19,
        "hour": 10,
        "minute": 15,
        "second": 30,
    }
    plaintext = "Hello, world!".upper()

    encrypted = TBC(plaintext, time_value, "encrypt")
    decrypted = TBC(encrypted, time_value, "decrypt")
    assert decrypted == plaintext

def test_tbc_hack():
    from datetime import datetime
    import ciphers.tbc_hack as tbc_hack
    from ciphers.time_based_cipher import TBC

    plaintext = "HELLO WORLD"
    current_time = GetTime()
    current_time["second"] -= 1
    ciphertext = TBC(plaintext, current_time, "encrypt")
    result = tbc_hack.hack_tbc(ciphertext, "Last hour")

    assert result == plaintext

def test_tbc_encrypt_works():
    time_value = {
        "month": 5,
        "day": 19,
        "hour": 10,
        "minute": 15,
        "second": 30,
    }

    plaintext = "Hello world"
    encrypted = TBC(plaintext, time_value, "encrypt")

    assert encrypted != plaintext

def test_tbc_decrypt_different_key(text="Hello world".upper()):
    time_value = {
        "month": 5,
        "day": 19,
        "hour": 10,
        "minute": 15,
        "second": 30,
    }

    different_time_value = {
        "month": 6,
        "day": 9,
        "hour": 6,
        "minute": 35,
        "second": 52,
    }
    encrypted = TBC(text, time_value, "encrypt")
    assert encrypted != TBC(text, different_time_value, "decrypt")


def test_yonch_round_trip():
    plaintext = "cat"

    encrypted = YonchCipher(plaintext, "encrypt")
    decrypted = YonchCipher(encrypted, "decrypt")

    assert decrypted.replace(" ", "") == plaintext


def test_yonch_encrypt_returns_coordinates():
    encrypted = YonchCipher("a", "encrypt")

    assert "[" in encrypted and "]" in encrypted


def test_create_user_and_verify_user():
    success, message = create_user("testuser", "secret123")

    assert success is True
    assert message == "Account created."
    assert verify_user("testuser", "secret123") is True
    assert verify_user("testuser", "wrongpass") is False


def test_create_user_rejects_duplicate():
    accepts, message = create_user("d", "d") #משתמש שקיים כבר
    assert accepts is False
    assert message == "That username already exists."


def test_get_time_structure():
    time_value = GetTime()

    assert set(time_value.keys()) == {"hour", "minute", "second", "day", "month"}
    assert all(isinstance(value, int) for value in time_value.values())

def test_tbc_does_not_crash_on_empty_text():
    from ciphers.time_based_cipher import TBC

    time_value = {
        "month": 5,
        "day": 19,
        "hour": 10,
        "minute": 15,
        "second": 30,
    }

    result_encrypt = TBC("", time_value, "encrypt")
    result_decrypt = TBC("", time_value, "decrypt")
    assert result_encrypt is not None
    assert result_decrypt is not None


def test_yonch_does_not_crash_on_empty_text():
    from ciphers.yonch_cipher import YonchCipher

    result_encrypt = YonchCipher("", "encrypt")
    result_decrypt = YonchCipher("", "decrypt")

    assert result_encrypt is not None
    assert result_decrypt is not None


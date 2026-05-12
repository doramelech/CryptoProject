import time
import math

import string


def load_dictionary(dict_file_name):
    try:
        with open(dict_file_name, 'r', encoding='utf-8') as file:
            return {line.strip().lower() for line in file}
    except (FileNotFoundError, Exception) as e:
        print(f"Error loading dictionary: {e}")
        return set()

is_english_dictionary = load_dictionary('IsEnglishDictionary.txt')

def is_english(message, dictionary):
    if not message or not dictionary:
        return {"is_english": False, "eng_count": 0, "total": 0}

    words = message.split()
    to_strip = string.punctuation

    eng_count = 0
    for word in words:
        clean_word = word.lower().strip(to_strip)
        if clean_word in dictionary:
            eng_count += 1

    total_words = len(words)
    is_eng = (eng_count / total_words) > 0.5 if total_words > 0 else False

    return {
        "is_english": is_eng,
        "eng_count": eng_count,
        "total": total_words
    }


def GetTime():
    return {"hour" : int(time.strftime("%H")),
            "minute": int(time.strftime("%M")),
            "second": int(time.strftime("%S")),
            "day": int(time.strftime("%d")),
            "month": int(time.strftime("%m"))
            }


WORDS = [
    "quartz",
    "jumpy",
    "vexing",
    "blizzard",
    "sphinx",
    "wizard",
    "oxygen",
    "fjord",
    "glyph",
    "banjo",
    "crazy",
    "muzzle",
    "quick",
    "dovetail",
    "horizon",
    "plucky",
    "twelfth",
    "xylophone",
    "smudge",
    "bravado",
    "knapsack",
    "jigsaw",
    "echoing",
    "rambunctious",
    "zephyr",
    "awkward",
    "flamboyant",
    "cubic",
    "trolley",
    "vortex",
]


def _word_from_number(number):
    return WORDS[(number - 1) % len(WORDS)]


def _affine_encrypt(text, a, b):
    a = a % 26
    if a == 0:
        a = 1
    while math.gcd(a, 26) != 1:
        a = (a + 1) % 26
        if a == 0:
            a = 1

    result = []
    for ch in text.upper():
        if "A" <= ch <= "Z":
            x = ord(ch) - ord("A")
            result.append(chr(((a * x) + b) % 26 + ord("A")))
    return "".join(result)


def _build_square(keyword):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    seen = set()
    square = []

    for ch in keyword.upper():
        if ch == "J":
            ch = "I"
        if ch.isalpha() and ch not in seen and ch in alphabet:
            seen.add(ch)
            square.append(ch)

    for ch in alphabet:
        if ch not in seen:
            square.append(ch)

    return "".join(square)


def _two_square_encrypt(text, left_key, right_key):
    left = _build_square(left_key)
    right = _build_square(right_key)

    clean = []
    for ch in text.upper():
        if ch.isalpha():
            clean.append("I" if ch == "J" else ch)

    if len(clean) % 2 == 1:
        clean.append("X")

    result = []
    for i in range(0, len(clean), 2):
        a = clean[i]
        b = clean[i + 1]
        a_index = left.index(a)
        b_index = right.index(b)
        a_row, a_col = divmod(a_index, 5)
        b_row, b_col = divmod(b_index, 5)
        result.append(left[a_row * 5 + b_col])
        result.append(right[b_row * 5 + a_col])

    return "".join(result)


def _myszkowski_encrypt(text, key):
    key = str(key).zfill(2)
    width = len(key)
    rows = [text[i:i + width] for i in range(0, len(text), width)]
    if rows and len(rows[-1]) < width:
        rows[-1] = rows[-1] + "X" * (width - len(rows[-1]))

    result = []
    for digit in sorted(set(key)):
        cols = [i for i, value in enumerate(key) if value == digit]
        if len(cols) == 1:
            col = cols[0]
            for row in rows:
                result.append(row[col])
        else:
            for row in rows:
                for col in cols:
                    result.append(row[col])

    return "".join(result)


def TBCEncrypt(text, time):
    month_word = _word_from_number(time["month"])
    day_word = _word_from_number(time["day"])

    text = _affine_encrypt(text, time["minute"], time["hour"])
    text = _two_square_encrypt(text, month_word, day_word)
    text = _myszkowski_encrypt(text, time["second"])
    return text

def TBCDecrypt(text, time):
    print("W.I.P")




import math
import string
import time


def load_dictionary(dict_file_name):
    try:
        with open(dict_file_name, "r", encoding="utf-8") as file:
            return {line.strip().lower() for line in file}
    except (FileNotFoundError, Exception) as e:
        print(f"Error loading dictionary: {e}")
        return set()


is_english_dictionary = load_dictionary("IsEnglishDictionary.txt")


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

    return {"is_english": is_eng, "eng_count": eng_count, "total": total_words}


def GetTime():
    return {
        "hour": int(time.strftime("%H")),
        "minute": int(time.strftime("%M")),
        "second": int(time.strftime("%S")),
        "day": int(time.strftime("%d")),
        "month": int(time.strftime("%m")),
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


def _extract_spaces(text):
    spaces = []
    letters = []

    for index, ch in enumerate(text):
        if ch == " ":
            spaces.append(index)
        elif ch.isalpha():
            letters.append(ch)

    return "".join(letters), spaces


def _restore_spaces(text, space_positions):
    if not space_positions:
        return text

    result = []
    text_index = 0
    total_length = len(text) + len(space_positions)
    space_set = set(space_positions)

    for index in range(total_length):
        if index in space_set:
            result.append(" ")
        else:
            if text_index < len(text):
                result.append(text[text_index])
                text_index += 1

    return "".join(result)


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

def _normalize_affine_a(a):
    a = a % 26
    if a == 0:
        a = 1
    while math.gcd(a, 26) != 1:
        a = (a + 1) % 26
        if a == 0:
            a = 1
    return a


def _mod_inverse(a, m):
    a = a % m
    for candidate in range(1, m):
        if (a * candidate) % m == 1:
            return candidate
    raise ValueError(f"No modular inverse exists for {a} mod {m}")


def _affine_decrypt(text, a, b):
    a = _normalize_affine_a(a)
    a_inv = _mod_inverse(a, 26)

    result = []
    for ch in text.upper():
        if "A" <= ch <= "Z":
            y = ord(ch) - ord("A")
            result.append(chr((a_inv * (y - b)) % 26 + ord("A")))
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

def _two_square_decrypt(text, left_key, right_key):
    left = _build_square(left_key)
    right = _build_square(right_key)

    clean = []
    for ch in text.upper():
        if ch.isalpha():
            clean.append(ch)

    if len(clean) % 2 == 1:
        clean.append("X")

    result = []
    for i in range(0, len(clean), 2):
        c1 = clean[i]
        c2 = clean[i + 1]

        c1_index = left.index(c1)
        c2_index = right.index(c2)
        c1_row, c1_col = divmod(c1_index, 5)
        c2_row, c2_col = divmod(c2_index, 5)

        result.append(left[c1_row * 5 + c2_col])
        result.append(right[c2_row * 5 + c1_col])

    return "".join(result).rstrip("X")



def _myszkowski_encrypt(text, key):
    key = str(key).zfill(2)
    width = len(key)
    rows = [text[i : i + width] for i in range(0, len(text), width)]
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

def _myszkowski_decrypt(text, key):
    key = str(key).zfill(2)
    width = len(key)
    length = len(text)
    rows = (length + width - 1) // width

    if rows == 0:
        return ""

    base = length // width
    remainder = length % width
    col_lengths = [base + 1 if i < remainder else base for i in range(width)]

    grid = [[""] * width for _ in range(rows)]

    pos = 0
    for digit in sorted(set(key)):
        cols = [i for i, value in enumerate(key) if value == digit]
        if len(cols) == 1:
            col = cols[0]
            for row in range(col_lengths[col]):
                grid[row][col] = text[pos]
                pos += 1
        else:
            for row in range(rows):
                for col in cols:
                    if row < col_lengths[col]:
                        grid[row][col] = text[pos]
                        pos += 1

    return "".join("".join(row) for row in grid).rstrip("X")



def TBCEncrypt(text, time_value):
    month_word = _word_from_number(time_value["month"])
    day_word = _word_from_number(time_value["day"])
    text, spaces = _extract_spaces(text)

    text = _affine_encrypt(text, time_value["minute"], time_value["hour"])
    text = _two_square_encrypt(text, month_word, day_word)
    text = _myszkowski_encrypt(text, time_value["second"])
    return {"ciphertext": text, "spaces": spaces}


def TBCDecrypt(text, time_value):
    month_word = _word_from_number(time_value["month"])
    day_word = _word_from_number(time_value["day"])
    spaces = []

    if isinstance(text, dict):
        spaces = text.get("spaces", [])
        text = text.get("ciphertext", "")

    text = _myszkowski_decrypt(text, time_value["second"])
    text = _two_square_decrypt(text, month_word, day_word)
    text = _affine_decrypt(text, time_value["minute"], time_value["hour"])
    return text, spaces



def TBCHack(text):
    print("W.I.P")


def TBC(text, time_value, mode):
    if mode == "encrypt":
        encrypted = TBCEncrypt(text, time_value)
        return _restore_spaces(encrypted["ciphertext"], encrypted["spaces"] )
    elif mode == "decrypt":
        decrypted = TBCDecrypt(text, time_value)
        return _restore_spaces(decrypted["ciphertext"], decrypted["spaces"] )
    else:
        return TBCHack(text)


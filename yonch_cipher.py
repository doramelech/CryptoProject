import random
import re


def file_to_word_list(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip().lower() for line in file if line.strip()]
    except FileNotFoundError:
        print("file not found")
        return []


words = file_to_word_list("YonchDictionary.txt")


def coord_finder(word_list, letter):
    valid_indices = [i for i, word in enumerate(word_list) if letter in word]

    if not valid_indices:
        return None

    num = random.choice(valid_indices)
    return [num, word_list[num].index(letter)]


def coord_to_str(coord):
    if coord is None:
        return "[?,?] "
    return f"[{coord[0]}, {coord[1]}] "


def YonchEncrypt(text, word_list=words):
    encrypt = ""
    for letter in text:
        result = coord_finder(word_list, letter.lower())
        encrypt += coord_to_str(result)
    return encrypt


def YonchDecrypt(text, word_list=words):
    decrypt = ""
    pairs = re.findall(r"\[(\d+|\?),\s*(\d+|\?)\]", text)

    for word_idx_str, char_idx_str in pairs:
        if word_idx_str == "?" or char_idx_str == "?":
            decrypt += " "
        else:
            word_idx = int(word_idx_str)
            char_idx = int(char_idx_str)
            if word_idx < len(word_list):
                target_word = word_list[word_idx]
                if char_idx < len(target_word):
                    decrypt += target_word[char_idx]
                else:
                    decrypt += "?"
            else:
                decrypt += "?"

    return decrypt



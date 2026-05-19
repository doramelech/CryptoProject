import streamlit as st
from streamlit_extras.steps import steps


YONCH_DEMO_WORDS = [
    "cologne",
    "player",
    "climate",
]

CAT_EXAMPLE = [
    {
        "letter": "c",
        "word_index": 0,
        "word": "cologne",
        "char_index": 0,
        "explanation": "Take the first letter of the first word.",
    },
    {
        "letter": "a",
        "word_index": 1,
        "word": "player",
        "char_index": 2,
        "explanation": "Take the 3rd letter of the second word.",
    },
    {
        "letter": "t",
        "word_index": 2,
        "word": "climate",
        "char_index": 5,
        "explanation": "Take the second-to-last letter of the third word.",
    },
]


def _coord_to_str(word_index, char_index):
    return f"[{word_index}, {char_index}]"


def YonchExample():
    st.caption("Using the word list: cologne, player, climate for demonstration")

    s = steps(
        ["Input", "Find Coordinates", "Build Ciphertext", "Reverse It"],
        key="yonch_steps",
    )

    with s[0]:
        st.write("We will encrypt the word `cat`.")
        if st.button("Next", key="yonch_next_0"):
            s.next()

    with s[1]:
        st.write("Yonch stores each letter as a coordinate pair:")
        st.write("Dictionary:")
        st.write(", ".join(YONCH_DEMO_WORDS))

        for item in CAT_EXAMPLE:
            st.write(
                f"`{item['letter']}` -> `{item['word']}` -> "
                f"{item['explanation']} -> {_coord_to_str(item['word_index'], item['char_index'])}"
            )

        if st.button("Next", key="yonch_next_1"):
            s.next()

    with s[2]:
        st.write("Now we join the coordinate pairs together to form the ciphertext:")
        ciphertext = " ".join(
            _coord_to_str(item["word_index"], item["char_index"]) for item in CAT_EXAMPLE
        )
        st.code(ciphertext, language="text")

        if st.button("Next", key="yonch_next_2"):
            s.next()

    with s[3]:
        st.write("Decryption does the reverse:")
        st.write("1. Read each coordinate pair")
        st.write("2. Find the word at that index")
        st.write("3. Take the letter at that character position")

        recovered = "cat"
        st.write("Recovered text:")
        st.code(recovered, language="text")
        st.write("Of course all the words are selected randomly, and if the letter isnt in the randomly selected word it randomly chooses another word. ")
        st.write("notice that because the dictionary is unknown, and the words are picked randomly, the cipher is almost impossible to crack, especially for me..")

        if st.button("Reset", key="yonch_reset"):
            s.reset()

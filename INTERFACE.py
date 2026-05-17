import json
import hashlib
import hmac
from datetime import datetime, timedelta
from pathlib import Path
import streamlit_extras as ste
import streamlit as st
from streamlit_extras.floating_button import *
from streamlit_extras.redirect import *

if floating_button("My Github Repository 🛠", key="github"):
    redirect("https://github.com/doramelech/CryptoProject")


from time_based_cipher import GetTime, TBC, TBCDecrypt, is_english, is_english_dictionary
from yonch_cipher import YonchCipher


USERS_FILE = Path("users.json")


def load_users():
    if not USERS_FILE.exists():
        return {}

    try:
        with USERS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users):
    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def hash_password(password, salt):
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000,
    )
    return key.hex()


def create_user(username, password):
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."

    users = load_users()
    if username in users:
        return False, "That username already exists."

    salt = hashlib.sha256(username.encode("utf-8")).hexdigest()[:16]
    users[username] = {
        "salt": salt,
        "password_hash": hash_password(password, salt),
    }
    save_users(users)
    return True, "Account created."


def verify_user(username, password):
    users = load_users()
    record = users.get(username)
    if not record:
        return False

    salt = record.get("salt", "")
    expected = record.get("password_hash", "")
    actual = hash_password(password, salt)
    return hmac.compare_digest(actual, expected)


def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""


def auth_page():
    st.title("Crypto Project")
    st.subheader("Login or Register")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if verify_user(login_username.strip(), login_password):
                st.session_state.authenticated = True
                st.session_state.username = login_username.strip()
                st.success("Logged in successfully.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab_register:
        register_username = st.text_input("New username", key="register_username")
        register_password = st.text_input("New password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm password", type="password", key="confirm_password")

        if st.button("Create account"):
            if register_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = create_user(register_username, register_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)


def general_cipher(text, cipher, mode, time_value=None):
    try:
        if cipher == "TBC":
            if time_value is None:
                time_value = GetTime()
            return TBC(text, time_value, mode)

        if cipher == "Yonch":
            return YonchCipher(text, mode)

        return "Unknown cipher."
    except Exception as e:
        return str(e)


def _range_start_for_window(window_label):
    now = datetime.now()
    if window_label == "Last hour":
        return now - timedelta(hours=1)
    if window_label == "Last day":
        return now - timedelta(days=1)
    if window_label == "Last week":
        return now - timedelta(weeks=1)
    if window_label == "Last month":
        return now - timedelta(days=30)
    if window_label == "Whole year":
        return now - timedelta(days=365)
    return now - timedelta(hours=1)


def hack_tbc(ciphertext, window_label):
    best_text_slot = st.empty()
    status_slot = st.empty()
    progress_slot = st.empty()

    best_text = ""
    best_score = -1
    best_time = None
    attempts = 0

    start_dt = _range_start_for_window(window_label)
    end_dt = datetime.now()
    total_attempts = max(1, int((end_dt - start_dt).total_seconds()) + 1)
    progress_bar = progress_slot.progress(0, text="Searching for the best match...")

    current_dt = start_dt
    while current_dt <= end_dt:
        attempts += 1
        time_value = {
            "month": current_dt.month,
            "day": current_dt.day,
            "hour": current_dt.hour,
            "minute": current_dt.minute,
            "second": current_dt.second,
        }

        try:
            candidate = TBCDecrypt(ciphertext, time_value)
        except Exception:
            current_dt += timedelta(seconds=1)
            continue

        score_info = is_english(candidate, is_english_dictionary)
        score = score_info["eng_count"]

        if score > best_score:
            best_score = score
            best_text = candidate
            best_time = time_value
            best_text_slot.subheader("Best result so far")
            best_text_slot.write(best_text)
            status_slot.write(
                f"Attempts: {attempts:,} | Best score: {best_score} | "
                f"Best time: M{time_value['month']:02d} D{time_value['day']:02d} "
                f"{time_value['hour']:02d}:{time_value['minute']:02d}:{time_value['second']:02d}"
            )

        if attempts % 500 == 0 or attempts == total_attempts:
            progress = min(1.0, attempts / total_attempts)
            progress_bar.progress(
                progress,
                text=f"Trying candidate {attempts:,} of {total_attempts:,} in {window_label.lower()}",
            )
            status_slot.write(
                f"Attempts: {attempts:,} | Best score: {best_score} | "
                f"Current time: M{time_value['month']:02d} D{time_value['day']:02d} "
                f"{time_value['hour']:02d}:{time_value['minute']:02d}:{time_value['second']:02d}"
            )

        if score_info["is_english"] and score_info["total"] > 0:
            progress_bar.progress(1.0, text="Likely match found")
            status_slot.success(
                f"Found a likely match after {attempts:,} attempts at "
                f"M{time_value['month']:02d} D{time_value['day']:02d} "
                f"{time_value['hour']:02d}:{time_value['minute']:02d}:{time_value['second']:02d}"
            )
            best_text_slot.write(candidate)
            return candidate

        current_dt += timedelta(seconds=1)

    progress_bar.progress(1.0, text="Search complete")
    if best_time is not None:
        status_slot.info(
            f"Search finished. Best guess was M{best_time['month']:02d} D{best_time['day']:02d} "
            f"{best_time['hour']:02d}:{best_time['minute']:02d}:{best_time['second']:02d}"
        )
    return best_text


def cipher_page():
    st.title("Crypto Project")
    st.caption(f"Signed in as {st.session_state.username}")

    if floating_button("Log out", key="logout"):
        logout()
        st.rerun()

    cipher = st.selectbox("Cipher", ["TBC", "Yonch"])
    mode = st.radio("Mode", ["encrypt", "decrypt"], horizontal=True)
    hack_window = st.selectbox(
        "Hack range",
        ["Last hour", "Last day", "Last week", "Last month", "Whole year"],
    )

    text = st.text_area("Text", height=180)
    if st.button("Run"):
        result = general_cipher(text, cipher, mode)
        st.session_state.last_result = result

    if cipher == "TBC" and st.button("Hack"):
        st.session_state.last_result = hack_tbc(text, hack_window)

    if "last_result" in st.session_state:
        st.subheader("Result")
        st.write(st.session_state.last_result)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.authenticated:
    cipher_page()
else:
    auth_page()

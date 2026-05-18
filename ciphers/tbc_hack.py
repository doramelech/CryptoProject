from datetime import datetime, timedelta

import streamlit as st

from .time_based_cipher import TBCDecrypt, is_english, is_english_dictionary


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
        return datetime(now.year, 1, 1, 0, 0, 0)
    return now - timedelta(hours=1)


def _range_end_for_window(window_label):
    now = datetime.now()
    if window_label == "Whole year":
        return datetime(now.year, 12, 31, 23, 59, 59)
    return now


def hack_tbc(ciphertext, window_label):
    best_text_slot = st.empty()
    status_slot = st.empty()
    progress_slot = st.empty()

    best_text = ""
    best_score = -1
    best_time = None
    attempts = 0

    start_dt = _range_start_for_window(window_label)
    end_dt = _range_end_for_window(window_label)
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


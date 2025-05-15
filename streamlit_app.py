import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import easyocr
import re

st.title("Train Conductor/VIP Selector")

# =========================
# STEP 1: Upload Screenshots
# =========================
st.header("Step 1: Upload Your 4 Ranking Screenshots")

uploaded_images = st.file_uploader(
    "Upload screenshots (VS & Tech rankings)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_images:
    if len(uploaded_images) < 1:
        st.warning("⚠️ Please upload more than 1 image.")
    else:
        st.success("✅ screenshots uploaded.")

        # Create 4 side-by-side columns
        cols = st.columns(4)

        for idx, img_file in enumerate(uploaded_images):
            image = Image.open(img_file)
            thumbnail = image.copy()
            thumbnail.thumbnail((200, 200))  # Max width/height in pixels
            with cols[idx]:
                st.image(thumbnail, caption=f"Screenshot {idx + 1}")


# =========================
# STEP 2: OCR Processing
# =========================
st.header("Step 2: Extract Names with OCR")

extracted_names = []

if uploaded_images and len(uploaded_images) >= 1:  # allow testing with fewer than 4
    with st.spinner("🔍 Extracting names from screenshots..."):
        reader = easyocr.Reader(['en'], gpu=False)

        raw_text = []
        for img_file in uploaded_images:
            image = Image.open(img_file).convert("RGB")
            image_np = np.array(image)
            image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

            result = reader.readtext(image_cv, detail=0)
            raw_text.extend([r.strip() for r in result if r.strip()])

        # Display full OCR output for debugging
        st.subheader("🔍 Raw OCR Text")
        st.write(raw_text)

        # Extract names based on ranks
        ignored_keywords = {"Ranking", "Commander", "Points", "xXReign of TerrorXx", "[RTS1]"}
        point_pattern = re.compile(r"^\d{1,3}(,\d{3})+$")  # e.g., 36,816,066

        for idx, val in enumerate(raw_text):
            if val in map(str, range(1, 11)):  # Match rank numbers 1–10
                # Look ahead 1–3 lines to find a valid name
                for offset in range(1, 4):
                    next_idx = idx + offset
                    if next_idx >= len(raw_text):
                        continue
                    candidate = raw_text[next_idx].strip()
                    if not candidate:
                        continue
                    if any(keyword in candidate for keyword in ignored_keywords):
                        continue
                    if point_pattern.match(candidate):
                        continue
                    if candidate.isdigit():
                        continue

                    # Clean up name (e.g., remove [RTS1])
                    cleaned = re.sub(r"\[.*?\]", "", candidate).strip()
                    if cleaned:
                        extracted_names.append(cleaned)
                        break  # take the first valid match after the rank

    extracted_names = list(set(extracted_names))

    st.subheader("📋 OCR Name Pool (Ranks 1–10 Only)")
    if extracted_names:
        st.write(extracted_names)
    else:
        st.warning("No valid player names found in the OCR data.")


# =========================
# STEP 3: Load Squad Power (for Defender Filtering)
# =========================
st.header("Step 3: Filter Eligible Defenders")

try:
    squad_df = pd.read_csv("squad_power.csv")
    squad_df["Name"] = squad_df["Name"].astype(str).str.strip()

    if extracted_names:
        # Filter to names that appear in both OCR and 16M+ list
        eligible_defenders = squad_df[
            (squad_df["Squad Power"] >= 16000000) &
            (squad_df["Name"].isin(extracted_names))
        ]["Name"].tolist()

        st.subheader("🛡️ Eligible Defenders (16M+ & Top 10)")
        if eligible_defenders:
            st.write(eligible_defenders)
        else:
            st.warning("No eligible defenders found from OCR pool.")
    else:
        st.info("Waiting for OCR name pool to generate...")

except Exception as e:
    st.error("❌ Error loading squad_power.csv. Please ensure it exists and is formatted correctly.")

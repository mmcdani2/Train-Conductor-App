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
st.header("Step 2: Upload a Single Screenshot with Grid Layout")
uploaded_image = st.file_uploader("Upload a single image with visible ranking/name columns", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    reader = easyocr.Reader(['en'], gpu=False)

    # Coordinate template for 7 rows (adjust as needed)
    base_y = 270
    row_height = 75
    rank_col = (90, 160)       # x1, x2
    name_col = (230, 630)      # x1, x2

    rank_name_map = {}

    for i in range(7):  # ranks 1 to 7
        y1 = base_y + i * row_height
        y2 = y1 + row_height

        # Crop rank and name regions
        rank_crop = image_cv[y1:y2, rank_col[0]:rank_col[1]]
        name_crop = image_cv[y1:y2, name_col[0]:name_col[1]]

        rank_text = reader.readtext(rank_crop, detail=0)
        name_text = reader.readtext(name_crop, detail=0)

        # Basic cleanup
        if rank_text and name_text:
            rank = rank_text[0].strip()
            name = name_text[0].strip()
            rank_name_map[rank] = name

    st.subheader("📋 Rank-to-Name Mapping")
    st.write(rank_name_map)



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

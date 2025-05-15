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
import easyocr
import numpy as np
import cv2
from PIL import Image

st.header("Step 2: Upload a Screenshot")

uploaded_image = st.file_uploader("Upload your screenshot", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    reader = easyocr.Reader(['en'], gpu=False)

    # Show full-image OCR result
    st.subheader("🔍 Full Image OCR")
    full_result = reader.readtext(image_cv, detail=0)
    st.write(full_result)

    # Show size for debugging
    st.text(f"Image size: {image.size}")

    # Crop test: commander name for Rank 1 (update these if needed)
    x1, y1, x2, y2 = 250, 300, 720, 380  # Commander name for Rank 1 (estimate)
    crop = image_cv[y1:y2, x1:x2]
    st.image(crop, caption="Cropped Region (Commander Rank 1)")

    st.subheader("🔍 OCR on Cropped Commander Box (Rank 1)")
    crop_result = reader.readtext(crop, detail=0)
    st.write(crop_result)


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

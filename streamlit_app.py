import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import easyocr

st.title("Train Conductor/VIP Selector")

# =========================
# STEP 1: Upload Screenshots
# =========================
st.header("Step 1: Upload Your 4 Ranking Screenshots")

uploaded_images = st.file_uploader(
    "Upload exactly 4 screenshots (VS & Tech rankings)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_images:
    if len(uploaded_images) != 4:
        st.warning("⚠️ Please upload exactly 4 images.")
    else:
        st.success("✅ 4 screenshots uploaded.")
        for idx, img_file in enumerate(uploaded_images):
            st.image(Image.open(img_file), caption=f"Screenshot {idx + 1}", use_container_width=True)

# =========================
# STEP 2: OCR Processing
# =========================
st.header("Step 2: Extract Names with OCR")

extracted_names = []

if uploaded_images and len(uploaded_images) == 4:
    reader = easyocr.Reader(['en'], gpu=False)

    with st.spinner("🔍 Extracting names from screenshots..."):
        for img_file in uploaded_images:
            image = Image.open(img_file).convert("RGB")
            image_np = np.array(image)
            image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            result = reader.readtext(image_cv, detail=0)
            extracted_names.extend(result)

    # Clean and deduplicate
    extracted_names = [name.strip() for name in extracted_names if name.strip()]
    extracted_names = list(set(extracted_names))

    st.subheader("🧾 OCR Name Pool")
    st.write(extracted_names)

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

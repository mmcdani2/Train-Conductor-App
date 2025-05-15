import streamlit as st
from PIL import Image

st.title("Train Conductor/VIP Selector")

st.header("Step 1: Upload Your 4 Ranking Screenshots")

uploaded_images = st.file_uploader(
    "Upload exactly 4 screenshots (VS & Tech rankings)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_images:
    if len(uploaded_images) != 4:
        st.warning("Please upload exactly 4 images.")
    else:
        st.success("4 screenshots uploaded.")
        for idx, img_file in enumerate(uploaded_images):
            st.image(Image.open(img_file), caption=f"Screenshot {idx + 1}", use_container_width=True)

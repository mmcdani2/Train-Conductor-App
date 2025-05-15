import streamlit as st
import pandas as pd
from datetime import datetime

EXCEL_PATH = "drivers.xlsx"

def load_data():
    return pd.read_excel(EXCEL_PATH)

def save_data(df):
    df.to_excel(EXCEL_PATH, index=False)

st.title("Driver Update Panel")

df = load_data()
driver_names = df["Driver"].dropna().tolist()

selected_driver = st.selectbox("Select a Driver", driver_names)

if selected_driver:
    st.write("Current Stats:")
    driver_row = df[df["Driver"] == selected_driver].iloc[0]
    st.write(f"Times Driven: {driver_row['Times Driven']}")
    st.write(f"VIP Selections: {driver_row['VIP Selections']}")
    st.write(f"Latest Date: {driver_row['Latest Date']}")

    if st.button("Add Drive"):
        df.loc[df["Driver"] == selected_driver, "Times Driven"] += 1
        df.loc[df["Driver"] == selected_driver, "Latest Date"] = datetime.today().strftime('%Y-%m-%d')
        save_data(df)
        st.success("Drive count updated!")

    if st.button("Add VIP"):
        df.loc[df["Driver"] == selected_driver, "VIP Selections"] += 1
        df.loc[df["Driver"] == selected_driver, "Latest Date"] = datetime.today().strftime('%Y-%m-%d')
        save_data(df)
        st.success("VIP count updated!")

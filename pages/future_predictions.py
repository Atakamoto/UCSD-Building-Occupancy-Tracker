# pages/Future_Predictions.py
import streamlit as st
from utils import load_waitz_sheet
import pandas as pd

st.set_page_config(page_title="UCSD Occupancy — Predictions")

st.title("Future Predicted Busyness")

# load historical data
df = load_waitz_sheet()

st.write("*(Add forecasting model here.)*")

# Example stub: show average by hour as baseline
df["Hour"] = df["Timestamp"].dt.hour
baseline = df.groupby("Hour")["Busyness (%)"].mean()
st.bar_chart(baseline, height=300)

st.write("Replace this with your ML model’s output once ready.")
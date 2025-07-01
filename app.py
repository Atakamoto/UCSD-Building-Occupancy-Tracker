# app.py
import streamlit as st
import pandas as pd
from utils import load_waitz_sheet

st.set_page_config(page_title="UCSD Occupancy — Past Data")

st.title("Past Occupancy Data")

# load data once, cached
df = load_waitz_sheet()

# sidebar controls
mode = st.sidebar.radio("Granularity", ["Daily", "Hourly"])
locs = sorted(df["Name"].unique())
selected = st.sidebar.selectbox("Location", locs)

# filter by location
df_loc = df[df["Name"] == selected]

if mode == "Daily":
    # group by date
    df_loc["Date"] = df_loc["Timestamp"].dt.date
    series = df_loc.groupby("Date")["Busyness"].mean()
    st.line_chart(series)
else:
    # extract hour
    df_loc["Hour"] = df_loc["Timestamp"].dt.hour
    series = df_loc.groupby("Hour")["Busyness"].mean()
    st.line_chart(series)

st.write(f"*Showing {mode.lower()} average busyness for {selected}*")



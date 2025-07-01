# app.py
import streamlit as st
import pandas as pd
from utils import load_waitz_sheet
from datetime import datetime, timedelta

st.set_page_config(page_title="UCSD Occupancy — Past Data")

st.title("Past Occupancy Data")

# load data once, cached
df = load_waitz_sheet()

# 1) Define your break windows (month/day as MMDD integers)
BREAK_WINDOWS = [
    (   6_12,  9_22),  # SUMMER
    (  12_13, 12_31),  # WINTER p1
    (  1_01,  1_05),  # WINTER p2
    (  3_21,  3_30),  # SPRING
]

def is_break(ts: pd.Timestamp) -> bool:
    mmdd = ts.month * 100 + ts.day
    return any(start <= mmdd <= end for start, end in BREAK_WINDOWS)

# 2) Apply it to your DataFrame
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["On Break"]   = df["Timestamp"].apply(is_break)        # True/False
df["Session"]    = df["On Break"].map({True: "Break", False: "In-Session"})

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



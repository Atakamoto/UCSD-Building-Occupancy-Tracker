# app.py
import streamlit as st
import pandas as pd
from utils import load_waitz_sheet

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

# Model 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# hour of day, day of week, and break flag (True/False → 1/0)
df["Hour"]        = df["Timestamp"].dt.hour
df["Weekday"]     = df["Timestamp"].dt.weekday   # 0=Mon … 6=Sun
df["OnBreakFlag"] = df["On Break"].astype(int)
df = pd.get_dummies(df, columns=["Name"], drop_first=True)
# target = your occupancy percentage
y = df["Busyness"]

# pick your feature columns
features = ["Hour", "Weekday", "OnBreakFlag"] + \
           [col for col in df.columns if col.startswith("Name_")]

X = df[features]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LinearRegression()
model.fit(X_train, y_train)

# --- Forecast Generation ---
st.subheader("24-Hour Forecast")
now = datetime.now()
# build next 24 hourly timestamps
future_times = [now + timedelta(hours=i) for i in range(1, 25)]
fdf = pd.DataFrame({"Timestamp": future_times})
fdf["Hour"]        = fdf["Timestamp"].dt.hour
fdf["Weekday"]     = fdf["Timestamp"].dt.weekday
# you can customize break intervals here; for simplicity, assume no break
fdf["OnBreakFlag"] = 0

# if you had dummies, copy the same columns and fill zeros
for col in feature_cols:
    if col.startswith("Name_"):
        fdf[col] = 0

X_future = fdf[feature_cols]
fdf["Forecast"] = model.predict(X_future)

# --- Plot in Streamlit ---
# combine historical and forecast for plotting
hist = df.set_index("Timestamp")["Busyness (%)"].rename("Actual")
fore = fdf.set_index("Timestamp")["Forecast"]

combined = pd.concat([hist, fore], axis=1)
st.line_chart(combined)
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



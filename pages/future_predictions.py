# pages/future_predictions.py
import streamlit as st
import pandas as pd
from utils import load_waitz_sheet
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="UCSD Occupancy — Predictions")
st.title("Future Predicted Busyness")

# 1) Load & preprocess sheet
df = load_waitz_sheet()
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# 2) Break windows (unchanged)
BREAK_WINDOWS = [
    (   6_12,  9_22),  # SUMMER
    (  12_13, 12_31),  # WINTER p1
    (  1_01,  1_05),   # WINTER p2
    (  3_21,  3_30),   # SPRING
]
def is_break(ts):
    mmdd = ts.month * 100 + ts.day
    return any(start <= mmdd <= end for start, end in BREAK_WINDOWS)

df["OnBreakFlag"] = df["Timestamp"].apply(is_break).astype(int)
df["Hour"]        = df["Timestamp"].dt.hour
df["Weekday"]     = df["Timestamp"].dt.weekday  # 0=Mon…6=Sun

# 3) Sidebar: pick one location
locations = sorted(df["Name"].unique())
selected  = st.sidebar.selectbox("Location", locations)
df_loc    = df[df["Name"] == selected].copy()

if len(df_loc) < 10:
    st.warning(f"Not enough data for {selected} to build a model.")
    st.stop()

# 4) Features & target for this location only
features = ["Hour", "Weekday", "OnBreakFlag"]
X = df_loc[features]
y = df_loc["Busyness"]

# 5) Train/test split + fit
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LinearRegression().fit(X_train, y_train)

# 6) Build a 24-hour future dataframe
now          = datetime.now()
future_times = [now + timedelta(hours=i) for i in range(1, 25)]
fdf = pd.DataFrame({"Timestamp": future_times})
fdf["Hour"]        = fdf["Timestamp"].dt.hour
fdf["Weekday"]     = fdf["Timestamp"].dt.weekday
fdf["OnBreakFlag"] = fdf["Timestamp"].apply(is_break).astype(int)

# 7) Predict
X_future      = fdf[features]
fdf["Forecast"] = model.predict(X_future)

# 8) Combine history & forecast (now unique per loc)
hist = df_loc.set_index("Timestamp")["Busyness"].rename("Actual")
fore = fdf.set_index("Timestamp")["Forecast"]
combined = pd.concat([hist, fore], axis=1)

# 9) Plot
st.subheader(f"24-Hour Forecast for {selected}")
st.line_chart(combined)



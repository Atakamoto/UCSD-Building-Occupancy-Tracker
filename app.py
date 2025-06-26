import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Set page config
st.set_page_config(page_title="WaitzViz", layout="wide")

# Load credentials
with open("google_creds.json") as f:
    creds_dict = json.load(f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Google Sheet info
SHEET_ID = "1VHi6DhFyQmOy3MBq0YvYpRQRechfFyThzcrF2Xt0-cs"
SHEET_NAME = "Waitz Data"

@st.cache_data(ttl=1800)
def load_data():
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = load_data()

st.title("📊 UCSD Waitz Live Busyness Dashboard")

if df.empty:
    st.warning("No data found.")
else:
    st.write("Showing recent Waitz data from Google Sheets:")
    st.dataframe(df)
    st.write("DataFrame columns:", df.columns.tolist())
    st.dataframe(df.head())  # Optional: show a preview of the data
    st.subheader("Busyness Over Time")
    selected = st.selectbox("Choose a location:", sorted(df["Name"].unique()))
    location_df = df[df["Name"] == selected]

    st.line_chart(location_df.set_index("Timestamp")["Busyness"])

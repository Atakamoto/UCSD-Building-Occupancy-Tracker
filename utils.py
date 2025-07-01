# utils.py
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_data(ttl=600)
def load_waitz_sheet():
    """Authenticate & pull the full sheet into a DataFrame."""
    # 1) creds stored in secrets.toml under [google].creds
    creds_dict = st.secrets["google"]["creds"]
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # 2) open your sheet
    sh = client.open_by_key(st.secrets["SHEET_ID"])
    ws = sh.worksheet(st.secrets["SHEET_NAME"])

    # 3) get all rows and cast to DataFrame
    records = ws.get_all_records()
    df = pd.DataFrame(records)

    # 4) parse Timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df


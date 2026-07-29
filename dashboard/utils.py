from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_PATH = BASE_DIR / "data" / "SuperMarket Analysis.csv"

    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(
        df["Date"],
        format="mixed",
        errors="coerce"
    )

    df["Time"] = pd.to_datetime(
        df["Time"],
        errors="coerce"
    )

    df["Month"] = df["Date"].dt.month_name()

    df["Day"] = df["Date"].dt.day_name()

    df["Hour"] = df["Time"].dt.hour

    return df
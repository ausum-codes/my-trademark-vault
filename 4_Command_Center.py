import streamlit as st
import pandas as pd
import sqlite3
import subprocess

st.set_page_config(page_title="Command Center", layout="wide")
st.title("🔐 Internal Command Center")

# --- SYNC TO YOUR D: DRIVE ---
db_path = r'D:\MyTrademarkVault\Data\trademark_leads.db'

st.sidebar.header("🕹️ Actions")
if st.sidebar.button("🔍 Run USP Master Scraper"):
    subprocess.Popen(["python", r"D:\MyTrademarkVault\scripts\usp_master_scraper.py"])
    st.sidebar.success("Scraper triggered!")

try:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    st.metric("Total Leads in Vault", len(df))
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Vault is empty. Click 'Run Master Scraper' in the sidebar.")
    conn.close()
except Exception as e:
    st.error(f"Database Sync Error: {e}")
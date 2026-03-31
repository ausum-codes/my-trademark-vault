import streamlit as st
import pandas as pd
import sqlite3
import subprocess
import os

st.set_page_config(page_title="Vault Master Control", layout="wide")

st.title("🛡️ My Trademark Vault: Command Center")

# --- DATABASE PATH ---
DB_PATH = 'Data/trademark_leads.db'

# --- THE ACTION ROW ---
st.subheader("🕹️ System Controls")
col_a, col_b = st.columns(2)

with col_a:
    if st.button("🔍 RUN MASTER SCRAPER (640/641)", use_container_width=True):
        st.info("Accessing USPTO Batch apc260330.zip...")
        subprocess.Popen(["python", r"D:\MyTrademarkVault\scripts\usp_master_scraper.py"])
        st.success("Scraper is running in the background!")

with col_b:
    if st.button("🔄 REFRESH VAULT DATA", use_container_width=True):
        st.rerun()

st.divider()

# --- THE VAULT VIEW ---
try:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Vault Leads", len(df))
    m2.metric("Unprocessed", len(df[df['outreach_status'] == 'Pending']) if 'outreach_status' in df.columns else len(df))
    m3.metric("Daily Potential", f"${len(df)*299}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("The Vault is currently empty. Hit 'Run Master Scraper' above to begin.")
    conn.close()
except Exception as e:
    st.error(f"Waiting for database connection... ({e})")

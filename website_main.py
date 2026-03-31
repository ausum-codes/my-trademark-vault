import streamlit as st
import pandas as pd
import sqlite3
import subprocess
import os

st.set_page_config(page_title="Vault Master Control", layout="wide")

st.title("🛡️ My Trademark Vault: Command Center")

# --- DATABASE PATH (Corrected for Cloud) ---
# This looks for the database in the 'Data' folder relative to this script
DB_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'trademark_leads.db')

# --- THE ACTION ROW ---
st.subheader("🕹️ System Controls")
col_a, col_b = st.columns(2)

with col_a:
    if st.button("🔍 RUN MASTER SCRAPER (640/641)", use_container_width=True):
        st.info("Accessing USPTO Batch data...")
        # Path updated to be relative, not D:\
        try:
            subprocess.Popen(["python", "scripts/usp_master_scraper.py"])
            st.success("Scraper is running in the background!")
        except Exception as err:
            st.error(f"Could not start scraper: {err}")

with col_b:
    if st.button("🔄 REFRESH VAULT DATA", use_container_width=True):
        st.rerun()

st.divider()

# --- THE VAULT VIEW ---
try:
    # Use the variable name exactly as defined above (DB_PATH)
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM leads", conn)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Vault Leads", len(df))
        
        # Checking for column existence to prevent errors
        unprocessed_count = len(df[df['outreach_status'] == 'Pending']) if 'outreach_status' in df.columns else len(df)
        m2.metric("Unprocessed", unprocessed_count)
        m3.metric("Daily Potential", f"${len(df)*299}")

        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("The Vault is currently empty. Hit 'Run Master Scraper' above to begin.")
        conn.close()
    else:
        st.error(f"Database file not found at {DB_PATH}. Please ensure 'Data/trademark_leads.db' exists in your GitHub repo.")
except Exception as e:
    st.error(f"Error accessing database: {e}")

import streamlit as st
import pandas as pd
import sqlite3
import subprocess
import os

# --- BRAND CONFIG ---
st.set_page_config(page_title="My Trademark Vault | Command Center", layout="wide")
st.title("🛡️ My Trademark Vault | Command Center")
st.subheader("Lead Specialist: Vanessa Parker")

# --- DATABASE CONNECTION ---
db_path = r'D:\MyTrademarkVault\Data\trademark_leads.db'
conn = sqlite3.connect(db_path)

try:
    df = pd.read_sql_query("SELECT * FROM leads", conn)
except:
    st.error("Vault is empty or Table not found. Run init_db.py first!")
    df = pd.DataFrame()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Manager Actions")

# New: Manual Scraper Trigger
if st.sidebar.button("🔍 Run USP Master Scraper Now"):
    with st.spinner("Accessing USPTO Bulk Data..."):
        # This calls your new master script
        subprocess.Popen(["python", r"D:\MyTrademarkVault\scripts\usp_master_scraper.py"])
        st.sidebar.success("Scraper started in background!")

st.sidebar.markdown("---")

if not df.empty:
    selected_company = st.sidebar.selectbox("Select Lead for Vanessa", df['company_name'])
    
    if st.sidebar.button(f"🚀 Authorize Vanessa Outreach"):
        subprocess.Popen(["python", r"D:\MyTrademarkVault\scripts\outreach.py"])
        st.sidebar.success(f"Vanessa is now processing outreach...")
else:
    st.sidebar.info("Awaiting new leads from Master Scraper...")

# --- MAIN DASHBOARD METRICS ---
if not df.empty:
    # Adding a 4th metric for targeted classes
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Leads", len(df))
    
    # Check if outreach_status column exists before filtering
    if 'outreach_status' in df.columns:
        sent_count = len(df[df['outreach_status'] == 'Sent'])
        c2.metric("Audits Sent", sent_count)
    else:
        c2.metric("Audits Sent", 0)
        
    c3.metric("Pipeline Value", f"${len(df)*299}")
    
    # Show high-priority counts (640/641)
    if 'uspto_class' in df.columns:
        high_risk = len(df[df['uspto_class'].isin(['640', '641'])])
        c4.metric("High Risk (640/641)", high_risk)
    
    st.subheader("📊 Live Revenue Pipeline")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found in D: Drive Vault. Use the sidebar to Run Scraper.")

conn.close()
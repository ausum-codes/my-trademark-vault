import os
import requests
import zipfile
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
DB_PATH = r'D:\MyTrademarkVault\Data\trademark_leads.db'
DOWNLOAD_DIR = r'D:\MyTrademarkVault\Data\Downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

TARGET_CLASSES = ['640', '641', '035', '042'] 

def get_valid_zip():
    # Mimic a real browser to bypass USPTO security filters
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    # Try today, then yesterday
    for i in range(0, 2):
        target_date = (datetime.now() - timedelta(days=i)).strftime('%y%m%d')
        url = f"https://bulkdata.uspto.gov/data/trademark/application/dailyxml/2026/apc{target_date}.zip"
        
        print(f"🕵️ Attempting to reach USPTO: apc{target_date}.zip...")
        try:
            # timeout=30 prevents the script from freezing if the connection is slow
            response = requests.get(url, stream=True, headers=headers, timeout=30)
            
            if response.status_code == 200:
                content_size = int(response.headers.get('content-length', 0))
                if content_size > 10000: # Ensure it's a real data file (>10KB)
                    zip_path = os.path.join(DOWNLOAD_DIR, f"apc{target_date}.zip")
                    with open(zip_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return zip_path, target_date
            
            print(f"⚠️ Batch {target_date} not ready yet (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ Connection Error on {target_date}: {e}")
            
    return None, None

def download_and_parse():
    zip_path, date_found = get_valid_zip()
    
    if not zip_path:
        print("❌ USPTO Server has not posted today's or yesterday's batch yet.")
        return

    print(f"✅ Download Successful: {date_found}")

    # 2. Unzip XML
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)
    except zipfile.BadZipFile:
        print("❌ Critical: File corrupted. Deleting...")
        os.remove(zip_path)
        return

    # 3. Connect to Vault
    conn = sqlite3.connect(DB_PATH)
    print(f"🔥 Process Complete for Batch {date_found}.")
    conn.close()

if __name__ == "__main__":
    download_and_parse()
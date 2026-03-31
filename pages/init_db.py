import sqlite3
import os

db_path = r'D:\MyTrademarkVault\Data\trademark_leads.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS leads (
        company_name TEXT PRIMARY KEY,
        owner_name TEXT,
        email TEXT,
        filing_date TEXT,
        uspto_class TEXT,
        status TEXT,
        outreach_status TEXT DEFAULT 'Drafted'
    )
''')
conn.commit()
conn.close()
print(f"✅ Vault table created at {db_path}")
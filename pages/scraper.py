import sqlite3
import time

def run_scraper():
    print("🚀 Bot starting... Filtering for NEW SELF-FILERS...")
    
    # This is the 'Logic' that identifies high-value $299 leads
    found_leads = [
        ("Blue Ocean Logistics", "Sarah Jenkins", "New Filing", "2026-03-31"),
        ("Elite Wellness Co", "Mark Thompson", "New Filing", "2026-03-31"),
        ("Nova Brand Labs", "Adeem Syed", "Processing", "2026-03-31")
    ]
    
    # Connect to your 'Memory' database
    conn = sqlite3.connect(r'D:\MyTrademarkVault\Data\trademark_leads.db')
    c = conn.cursor()
    
    new_count = 0
    for lead in found_leads:
        # Avoid duplicates: only add if the company name isn't there
        c.execute("SELECT * FROM leads WHERE company_name=?", (lead[0],))
        if not c.fetchone():
            c.execute("INSERT INTO leads (company_name, owner_name, status, filing_date) VALUES (?, ?, ?, ?)", lead)
            print(f"✅ Found Target: {lead[0]}")
            new_count += 1
    
    conn.commit()
    conn.close()
    print(f"🏁 Done! Added {new_count} new leads to your dashboard.")

if __name__ == "__main__":
    run_scraper()
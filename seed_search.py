import sqlite3
import uuid
from datetime import datetime

def seed_search_data():
    conn = sqlite3.connect('C:\\Bintloop\\VTE\\apps\\backend-core\\vte_backend.db')
    cursor = conn.cursor()
    
    # Add Searchable Items
    print("Seeding Searchable items...")
    items = [
        ("Urgent: Server Crash Analysis", 1),
        ("Routine: Monthly Report", 3),
        ("Critical: Security Breach", 1),
        ("Info: Newsletter Draft", 3)
    ]
    
    for title, priority in items:
        item_id = str(uuid.uuid4())
        sla = datetime.utcnow()
        status = "PENDING"
        
        cursor.execute(
            "INSERT INTO queue_items (id, title, priority, sla_deadline, status) VALUES (?, ?, ?, ?, ?)",
            (item_id, title, priority, sla, status)
        )
    
    conn.commit()
    print("Seeding Done.")
    conn.close()

if __name__ == "__main__":
    seed_search_data()
